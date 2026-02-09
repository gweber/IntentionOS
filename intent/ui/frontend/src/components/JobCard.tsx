import { Link } from 'react-router-dom'
import type { Job } from '../lib/api'
import { formatDateTime } from '../lib/time'

function statusClasses(status: Job['status']) {
  switch (status) {
    case 'queued':
      return 'bg-zinc-200 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-100'
    case 'running':
      return 'bg-blue-200 text-blue-900 dark:bg-blue-950 dark:text-blue-200'
    case 'completed':
      return 'bg-emerald-200 text-emerald-900 dark:bg-emerald-950 dark:text-emerald-200'
    case 'failed':
      return 'bg-rose-200 text-rose-900 dark:bg-rose-950 dark:text-rose-200'
    case 'cancelled':
      return 'bg-amber-200 text-amber-900 dark:bg-amber-950 dark:text-amber-200'
  }
}

export default function JobCard(props: { job: Job }) {
  const { job } = props
  return (
    <Link
      to={`/jobs/${job.id}`}
      className="group block rounded-2xl border border-zinc-200 bg-white p-4 shadow-card transition hover:-translate-y-0.5 hover:border-zinc-300 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-700"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold">{job.kind.toUpperCase()} job</div>
          <div className="mt-1 font-mono text-xs text-zinc-600 dark:text-zinc-400">
            {job.id}
          </div>
        </div>
        <span className={`rounded-full px-2 py-1 text-xs font-medium ${statusClasses(job.status)}`}>
          {job.status}
        </span>
      </div>
      <div className="mt-3 text-xs text-zinc-600 dark:text-zinc-400">
        Created: {formatDateTime(job.created_at)}
      </div>
      {job.last_event ? (
        <div className="mt-2 line-clamp-2 text-sm text-zinc-800 dark:text-zinc-100">
          <span className="mr-2 rounded bg-zinc-100 px-1.5 py-0.5 font-mono text-[11px] text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
            {job.last_event.type}
          </span>
          {job.last_event.message}
        </div>
      ) : (
        <div className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">No events yet</div>
      )}
      {job.status === 'running' ? (
        <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-zinc-100 dark:bg-zinc-800">
          <div className="h-full w-1/2 animate-pulse rounded-full bg-gradient-to-r from-indigo-500 to-cyan-400" />
        </div>
      ) : null}
      <div className="mt-3 text-xs text-zinc-500 group-hover:text-zinc-700 dark:text-zinc-500 dark:group-hover:text-zinc-300">
        Open →
      </div>
    </Link>
  )
}
