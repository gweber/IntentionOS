export const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export type JobStatus = 'queued' | 'running' | 'completed' | 'failed' | 'cancelled'

export type JobKind = 'demo'

export type JobEventType = 'status' | 'thought' | 'log' | 'result' | 'error'

export type JobEvent = {
  timestamp: string
  job_id: string
  type: JobEventType
  message: string
  payload?: Record<string, unknown> | null
}

export type Job = {
  id: string
  kind: JobKind
  status: JobStatus
  created_at: string
  started_at?: string | null
  finished_at?: string | null
  result?: Record<string, unknown> | null
  error?: string | null
  last_event?: JobEvent | null
}

export async function health(): Promise<{ ok: boolean }> {
  const r = await fetch(`${API_URL}/health`)
  if (!r.ok) throw new Error(`health failed: ${r.status}`)
  return r.json()
}

export async function listJobs(): Promise<Job[]> {
  const r = await fetch(`${API_URL}/jobs`)
  if (!r.ok) throw new Error(`list jobs failed: ${r.status}`)
  return r.json()
}

export async function createDemoJob(input: Record<string, unknown> = {}): Promise<Job> {
  const r = await fetch(`${API_URL}/jobs`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ kind: 'demo', input }),
  })
  if (!r.ok) throw new Error(`create job failed: ${r.status}`)
  return r.json()
}

export async function getJob(jobId: string): Promise<Job> {
  const r = await fetch(`${API_URL}/jobs/${jobId}`)
  if (!r.ok) throw new Error(`get job failed: ${r.status}`)
  return r.json()
}

export async function cancelJob(jobId: string): Promise<Job> {
  const r = await fetch(`${API_URL}/jobs/${jobId}/cancel`, { method: 'POST' })
  if (!r.ok) throw new Error(`cancel job failed: ${r.status}`)
  return r.json()
}

export function jobEventsUrl(jobId: string): string {
  return `${API_URL}/jobs/${jobId}/events`
}
