import React, { useMemo, useRef } from 'react'
import type { JobEvent } from '../lib/api'
import { formatTime } from '../lib/time'
import type { EventFilters } from './EventFilterBar'

function typeBadgeClasses(t: JobEvent['type']): string {
  switch (t) {
    case 'status':
      return 'bg-zinc-200 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-100'
    case 'thought':
      return 'bg-indigo-200 text-indigo-900 dark:bg-indigo-950 dark:text-indigo-200'
    case 'log':
      return 'bg-sky-200 text-sky-900 dark:bg-sky-950 dark:text-sky-200'
    case 'result':
      return 'bg-emerald-200 text-emerald-900 dark:bg-emerald-950 dark:text-emerald-200'
    case 'error':
      return 'bg-rose-200 text-rose-900 dark:bg-rose-950 dark:text-rose-200'
  }
}

function matchesQuery(ev: JobEvent, query: string): boolean {
  const q = query.trim().toLowerCase()
  if (!q) return true
  const payload = ev.payload ? JSON.stringify(ev.payload).toLowerCase() : ''
  return (
    ev.type.toLowerCase().includes(q) ||
    ev.message.toLowerCase().includes(q) ||
    payload.includes(q)
  )
}

export default function JobTimeline(props: {
  events: JobEvent[]
  filters: EventFilters
  autoScroll: boolean
  cap: number
  onLoadMore: () => void
}) {
  const containerRef = useRef<HTMLDivElement | null>(null)

  const filtered = useMemo(() => {
    const out = props.events.filter(
      (e) => props.filters.types.has(e.type) && matchesQuery(e, props.filters.query),
    )
    return out
  }, [props.events, props.filters])

  // auto-scroll on updates
  React.useEffect(() => {
    if (!props.autoScroll) return
    const el = containerRef.current
    if (!el) return
    el.scrollTop = el.scrollHeight
  }, [filtered.length, props.autoScroll])

  const visible = filtered.slice(-props.cap)
  const hiddenCount = Math.max(0, filtered.length - visible.length)

  return (
    <div className="flex h-full flex-col">
      {hiddenCount > 0 ? (
        <div className="mb-2 flex items-center justify-between text-xs text-zinc-600 dark:text-zinc-400">
          <div>
            Showing last {visible.length} of {filtered.length} matching events
          </div>
          <button
            type="button"
            onClick={props.onLoadMore}
            className="rounded-md border border-zinc-200 bg-white px-2 py-1 hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800"
          >
            Load more
          </button>
        </div>
      ) : null}

      <div
        ref={containerRef}
        className="flex-1 overflow-auto rounded-xl border border-zinc-200 bg-white p-3 dark:border-zinc-800 dark:bg-zinc-900"
      >
        <ul className="space-y-2">
          {visible.map((ev, idx) => (
            <li key={`${ev.timestamp}-${idx}`} className="flex gap-3">
              <div className="w-[84px] shrink-0 font-mono text-xs text-zinc-500 dark:text-zinc-400">
                {formatTime(ev.timestamp)}
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-start gap-2">
                  <span
                    className={`shrink-0 rounded px-2 py-0.5 font-mono text-[11px] ${typeBadgeClasses(
                      ev.type,
                    )}`}
                  >
                    {ev.type}
                  </span>
                  <div className="min-w-0 break-words text-sm">{ev.message}</div>
                </div>
                {ev.payload ? (
                  <pre className="mt-1 overflow-auto rounded-lg bg-zinc-50 p-2 text-xs text-zinc-700 dark:bg-zinc-950 dark:text-zinc-200">
                    {JSON.stringify(ev.payload, null, 2)}
                  </pre>
                ) : null}
              </div>
            </li>
          ))}
        </ul>
        {visible.length === 0 ? (
          <div className="py-10 text-center text-sm text-zinc-500 dark:text-zinc-400">No events</div>
        ) : null}
      </div>
    </div>
  )
}
