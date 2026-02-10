import { API_URL } from './api'
import { useState } from 'react';

export type Provider = 'openai_compatible' | 'anthropic' | 'google'

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

// Store and expose state
const configStore = {
  profiles: [] as LlmProfile[],
  activeProfile: null as LlmProfile | null,
  config: null as IntentConfig | null,

  async load() {
    const config = await getConfig()
    this.config = config
    this.profiles = config.llms.profiles
    this.activeProfile = config.llms.profiles.find(p => p.id === config.llms.active) || null
    return this
  },

  async updateProfile(id: string, data: Partial<LlmProfile>) {
    const profile = this.profiles.find(p => p.id === id)
    if (!profile) throw new Error(`Profile not found: ${id}`)
    Object.assign(profile, data)
    this.config!.llms.profiles = this.profiles
    await saveConfig(this.config!)
    return this
  },

  async setActiveProfile(id: string) {
    const profile = this.profiles.find(p => p.id === id)
    if (!profile) throw new Error(`Profile not found: ${id}`)
    this.config!.llms.active = id
    await saveConfig(this.config!)
    this.activeProfile = profile
    return this
  },

  async addProfile(profile: LlmProfile) {
    this.profiles.push(profile)
    this.config!.llms.profiles = this.profiles
    await saveConfig(this.config!)
    return this
  },

  async removeProfile(id: string) {
    const index = this.profiles.findIndex(p => p.id === id)
    if (index === -1) throw new Error(`Profile not found: ${id}`)
    this.profiles.splice(index, 1)
    this.config!.llms.profiles = this.profiles
    await saveConfig(this.config!)
    return this
  },

  async reset() {
    this.config = null
    this.profiles = []
    this.activeProfile = null
    return this
  }
}

// Export a React hook
export const useConfigStore = () => {
  const [state, setState] = useState({
    profiles: configStore.profiles,
    activeProfile: configStore.activeProfile,
    config: configStore.config
  })

  const load = async () => {
    const config = await configStore.load()
    setState({
      profiles: config.profiles,
      activeProfile: config.activeProfile,
      config: config.config
    })
  }

  const updateProfile = async (id: string, data: Partial<LlmProfile>) => {
    const config = await configStore.updateProfile(id, data)
    setState({
      profiles: config.profiles,
      activeProfile: config.activeProfile,
      config: config.config
    })
  }

  const setActiveProfile = async (id: string) => {
    const config = await configStore.setActiveProfile(id)
    setState({
      profiles: config.profiles,
      activeProfile: config.activeProfile,
      config: config.config
    })
  }

  const addProfile = async (profile: LlmProfile) => {
    const config = await configStore.addProfile(profile)
    setState({
      profiles: config.profiles,
      activeProfile: config.activeProfile,
      config: config.config
    })
  }

  const removeProfile = async (id: string) => {
    const config = await configStore.removeProfile(id)
    setState({
      profiles: config.profiles,
      activeProfile: config.activeProfile,
      config: config.config
    })
  }

  return {
    profiles: state.profiles,
    activeProfile: state.activeProfile,
    config: state.config,
    load,
    updateProfile,
    setActiveProfile,
    addProfile,
    removeProfile
  }
}

// Export store instance
export default configStore;
