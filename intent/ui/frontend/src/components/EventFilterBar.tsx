import type { JobEventType } from '../lib/api'

const ALL_TYPES: JobEventType[] = ['status', 'thought', 'log', 'result', 'error']

export type EventFilters = {
  types: Set<JobEventType>
  query: string
}

export default function EventFilterBar(props: {
  filters: EventFilters
  onChange: (f: EventFilters) => void
}) {
  const { filters, onChange } = props

  function toggleType(t: JobEventType) {
    const next = new Set(filters.types)
    if (next.has(t)) next.delete(t)
    else next.add(t)
    onChange({ ...filters, types: next })
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      <div className="flex flex-wrap gap-2" role="group" aria-label="Event type filters">
        {ALL_TYPES.map((t) => {
          const active = filters.types.has(t)
          return (
            <button
              key={t}
              type="button"
              onClick={() => toggleType(t)}
              className={
                active
                  ? 'rounded-full bg-zinc-900 px-3 py-1 text-xs font-medium text-white dark:bg-zinc-100 dark:text-zinc-900'
                  : 'rounded-full border border-zinc-200 bg-white px-3 py-1 text-xs text-zinc-700 hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-200 dark:hover:bg-zinc-800'
              }
              aria-pressed={active}
            >
              {t}
            </button>
          )
        })}
      </div>

      <div className="ml-auto flex w-full items-center gap-2 sm:w-auto">
        <label className="sr-only" htmlFor="event-search">
          Search events
        </label>
        <input
          id="event-search"
          value={filters.query}
          onChange={(e) => onChange({ ...filters, query: e.target.value })}
          placeholder="Search…"
          className="w-full rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm shadow-sm dark:border-zinc-800 dark:bg-zinc-900"
        />
      </div>
    </div>
  )
}
