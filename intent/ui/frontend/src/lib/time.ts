export function formatTime(ts: string): string {
  const d = new Date(ts)
  return d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

export function formatDateTime(ts: string): string {
  const d = new Date(ts)
  return d.toLocaleString()
}
