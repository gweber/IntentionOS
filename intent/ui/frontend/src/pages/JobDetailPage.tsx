import { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { cancelJob, getJob, jobEventsUrl, type Job, type JobEvent, type JobEventType } from '../lib/api'
import EventFilterBar, { type EventFilters } from '../components/EventFilterBar'
import JobTimeline from '../components/JobTimeline'

const ALL_TYPES: JobEventType[] = ['status', 'thought', 'log', 'result', 'error']

export default function JobDetailPage() {
  const { jobId } = useParams()
  const navigate = useNavigate()

  const [job, setJob] = useState<Job | null>(null)
  const [events, setEvents] = useState<JobEvent[]>([])
  const [error, setError] = useState<string | null>(null)
  const [autoScroll, setAutoScroll] = useState(true)
  const [cap, setCap] = useState(200)
  const [filters, setFilters] = useState<EventFilters>(() => ({
    types: new Set(ALL_TYPES),
    query: '',
  }))

  const sourceRef = useRef<EventSource | null>(null)

  useEffect(() => {
    if (!jobId) return
    ;(async () => {
      try {
        setError(null)
        setEvents([])
        const j = await getJob(jobId)
        setJob(j)
      } catch (e) {
        setError(e instanceof Error ? e.message : 'failed to load job')
      }
    })()
  }, [jobId])

  useEffect(() => {
    if (!jobId) return
    // connect SSE
    const url = jobEventsUrl(jobId)
    const es = new EventSource(url)
    sourceRef.current = es

    es.addEventListener('message', (m) => {
      try {
        const ev = JSON.parse((m as MessageEvent).data) as JobEvent
        setEvents((prev) => {
          const next = [...prev, ev]
          // keep memory bounded
          return next.length > 4000 ? next.slice(-4000) : next
        })
        // update job summary based on event types
        if (ev.type === 'status') {
          // fetch job detail when status changes (cheap)
          getJob(jobId).then(setJob).catch(() => {})
        }
      } catch {
        // ignore malformed
      }
    })

    es.onerror = () => {
      // show a soft error but keep trying (EventSource reconnects automatically)
      setError('SSE connection lost. Reconnecting…')
    }

    return () => {
      es.close()
      sourceRef.current = null
    }
  }, [jobId])

  const thoughtEvents = useMemo(
    () => {
      if (!filters.types.has('thought')) return []
      const q = filters.query.trim().toLowerCase()
      return events.filter((e) => {
        if (e.type !== 'thought') return false
        if (!q) return true
        const payload = e.payload ? JSON.stringify(e.payload).toLowerCase() : ''
        return e.message.toLowerCase().includes(q) || payload.includes(q)
      })
    },
    [events, filters.query, filters.types],
  )

  async function onCancel() {
    if (!jobId) return
    try {
      await cancelJob(jobId)
      const j = await getJob(jobId)
      setJob(j)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'failed to cancel')
    }
  }

  if (!jobId) {
    return (
      <div className="rounded-xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">
        Missing job id
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <button
            type="button"
            onClick={() => navigate('/')}
            className="text-sm text-zinc-600 hover:underline dark:text-zinc-400"
          >
            ← Back
          </button>
          <h1 className="mt-1 text-lg font-semibold">Job</h1>
          <div className="mt-1 font-mono text-xs text-zinc-600 dark:text-zinc-400">{jobId}</div>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={autoScroll}
              onChange={(e) => setAutoScroll(e.target.checked)}
            />
            Auto-scroll
          </label>
          <button
            type="button"
            onClick={onCancel}
            disabled={!job || !['queued', 'running'].includes(job.status)}
            className="rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm shadow-sm hover:bg-zinc-50 disabled:opacity-50 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800"
          >
            Cancel
          </button>
        </div>
      </div>

      {job ? (
        <div className="grid gap-4 lg:grid-cols-3">
          <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900 lg:col-span-2">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-sm font-semibold">Timeline</div>
                <div className="mt-1 text-xs text-zinc-600 dark:text-zinc-400">
                  Status: <span className="font-medium">{job.status}</span>
                </div>
              </div>
              <div className="text-right text-xs text-zinc-600 dark:text-zinc-400">
                <div>Events: {events.length}</div>
                <div>Showing: last {cap}</div>
              </div>
            </div>

            <div className="mt-3">
              <EventFilterBar filters={filters} onChange={setFilters} />
            </div>

            <div className="mt-3 h-[520px]">
              <JobTimeline
                events={events}
                filters={filters}
                autoScroll={autoScroll}
                cap={cap}
                onLoadMore={() => setCap((c) => Math.min(2000, c + 200))}
              />
            </div>
          </div>

          <div className="space-y-4">
            <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900">
              <div className="text-sm font-semibold">Thinking trace</div>
              <div className="mt-2 max-h-[260px] overflow-auto rounded-xl border border-zinc-200 bg-zinc-50 p-3 font-mono text-xs leading-5 text-zinc-800 dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-100">
                {thoughtEvents.length === 0 ? (
                  <div className="text-zinc-500">No thought events yet</div>
                ) : (
                  <ul className="space-y-1">
                    {thoughtEvents.slice(-300).map((e, idx) => (
                      <li key={`${e.timestamp}-${idx}`} className="break-words">
                        {e.message}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              <div className="mt-2 text-xs text-zinc-600 dark:text-zinc-400">
                Tip: use the search box to filter events.
              </div>
            </div>

            <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900">
              <div className="text-sm font-semibold">Result</div>
              {job.result ? (
                <pre className="mt-2 overflow-auto rounded-xl bg-zinc-50 p-3 text-xs text-zinc-800 dark:bg-zinc-950 dark:text-zinc-100">
                  {JSON.stringify(job.result, null, 2)}
                </pre>
              ) : job.error ? (
                <div className="mt-2 rounded-md border border-rose-200 bg-rose-50 p-2 text-sm text-rose-900 dark:border-rose-900/40 dark:bg-rose-950/30 dark:text-rose-200">
                  {job.error}
                </div>
              ) : (
                <div className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">No result yet</div>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="rounded-xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">
          Loading…
        </div>
      )}

      {error ? (
        <div className="rounded-md border border-amber-200 bg-amber-50 p-2 text-sm text-amber-900 dark:border-amber-900/40 dark:bg-amber-950/30 dark:text-amber-200">
          {error}
        </div>
      ) : null}
    </div>
  )
}
