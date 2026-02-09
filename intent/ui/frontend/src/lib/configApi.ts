import { API_URL } from './api'

export type Provider = 'openai' | 'openai_compatible' | 'anthropic_compatible'

export type LlmProfile = {
  id: string
  label: string
  provider: Provider
  base_url: string
  model: string
  api_key_env: string
  headers?: Record<string, string>
}

export type IntentConfig = {
  version: 1
  llms: {
    active: string
    profiles: LlmProfile[]
  }
}

async function httpJson<T>(url: string, init?: RequestInit): Promise<T> {
  const r = await fetch(url, init)
  if (!r.ok) {
    const txt = await r.text().catch(() => '')
    throw new Error(`${r.status} ${r.statusText}${txt ? `: ${txt}` : ''}`)
  }
  return r.json() as Promise<T>
}

export async function getConfig(): Promise<IntentConfig> {
  return httpJson<IntentConfig>(`${API_URL}/api/config`)
}

export async function saveConfig(config: IntentConfig): Promise<IntentConfig> {
  return httpJson<IntentConfig>(`${API_URL}/api/config`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ config }),
  })
}

export async function testProfile(profileId: string, config?: IntentConfig): Promise<any> {
  return httpJson(`${API_URL}/api/config/test/${encodeURIComponent(profileId)}`, {
    method: 'POST',
    headers: config ? { 'content-type': 'application/json' } : undefined,
    body: config ? JSON.stringify({ config }) : undefined,
  })
}
