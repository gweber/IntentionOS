import { useEffect, useMemo, useState } from 'react'
import { createDemoJob, listJobs, type Job } from '../lib/api'
import JobCard from '../components/JobCard'

export default function DashboardPage() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [topic, setTopic] = useState('bento')
  const [creating, setCreating] = useState(false)

  async function refresh() {
    try {
      setError(null)
      const j = await listJobs()
      setJobs(j)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'failed to load')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
    const t = window.setInterval(refresh, 2000)
    return () => window.clearInterval(t)
  }, [])

  const runningCount = useMemo(() => jobs.filter((j) => j.status === 'running').length, [jobs])

  async function onCreate() {
    setCreating(true)
    try {
      await createDemoJob({ topic })
      await refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'failed to create')
    } finally {
      setCreating(false)
    }
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900 md:col-span-2">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h1 className="text-lg font-semibold">Dashboard</h1>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                Create demo jobs and watch live updates.
              </p>
            </div>
            <button
              type="button"
              onClick={refresh}
              className="rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm shadow-sm hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800"
            >
              Refresh
            </button>
          </div>

          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            <div className="rounded-xl border border-zinc-200 bg-zinc-50 p-3 dark:border-zinc-800 dark:bg-zinc-950">
              <div className="text-xs text-zinc-600 dark:text-zinc-400">Jobs</div>
              <div className="text-2xl font-semibold">{jobs.length}</div>
            </div>
            <div className="rounded-xl border border-zinc-200 bg-zinc-50 p-3 dark:border-zinc-800 dark:bg-zinc-950">
              <div className="text-xs text-zinc-600 dark:text-zinc-400">Running</div>
              <div className="text-2xl font-semibold">{runningCount}</div>
            </div>
            <div className="rounded-xl border border-zinc-200 bg-zinc-50 p-3 dark:border-zinc-800 dark:bg-zinc-950">
              <div className="text-xs text-zinc-600 dark:text-zinc-400">Backend</div>
              <div className="text-sm font-medium">http://localhost:8000</div>
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900">
          <h2 className="text-sm font-semibold">Create demo job</h2>
          <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
            Emits status/log/thought events every ~200–600ms.
          </p>

          <label className="mt-4 block text-xs text-zinc-600 dark:text-zinc-400" htmlFor="topic">
            Topic
          </label>
          <input
            id="topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="mt-1 w-full rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm dark:border-zinc-800 dark:bg-zinc-900"
          />

          <button
            type="button"
            onClick={onCreate}
            disabled={creating}
            className="mt-4 w-full rounded-md bg-zinc-900 px-3 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-zinc-800 disabled:opacity-60 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200"
          >
            {creating ? 'Creating…' : 'Create'}
          </button>

          {error ? (
            <div className="mt-3 rounded-md border border-rose-200 bg-rose-50 p-2 text-sm text-rose-900 dark:border-rose-900/40 dark:bg-rose-950/30 dark:text-rose-200">
              {error}
            </div>
          ) : null}
        </div>
      </section>

      <section>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold">Jobs</h2>
          {loading ? <div className="text-xs text-zinc-500">Loading…</div> : null}
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>

        {!loading && jobs.length === 0 ? (
          <div className="mt-10 text-center text-sm text-zinc-500 dark:text-zinc-400">
            No jobs yet. Create a demo job to see live streaming events.
          </div>
        ) : null}
      </section>
    </div>
  )
}
