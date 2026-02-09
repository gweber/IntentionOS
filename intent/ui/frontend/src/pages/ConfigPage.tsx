import { useEffect, useMemo, useState } from 'react'
import {
  getConfig,
  saveConfig,
  testProfile,
  type LlmProfile,
  type IntentConfig,
  type Provider,
} from '../lib/configApi'

type TestState = { status: 'idle' | 'testing' | 'ok' | 'error'; message?: string }

function TextField(props: {
  label: string
  value: string
  onChange: (v: string) => void
  placeholder?: string
}) {
  return (
    <label className="block">
      <div className="text-xs font-medium text-zinc-600 dark:text-zinc-400">{props.label}</div>
      <input
        value={props.value}
        onChange={(e) => props.onChange(e.target.value)}
        placeholder={props.placeholder}
        className="mt-1 w-full rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm dark:border-zinc-800 dark:bg-zinc-900"
      />
    </label>
  )
}

function SelectField<T extends string>(props: {
  label: string
  value: T
  options: { value: T; label: string }[]
  onChange: (v: T) => void
}) {
  return (
    <label className="block">
      <div className="text-xs font-medium text-zinc-600 dark:text-zinc-400">{props.label}</div>
      <select
        value={props.value}
        onChange={(e) => props.onChange(e.target.value as T)}
        className="mt-1 w-full rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm dark:border-zinc-800 dark:bg-zinc-900"
      >
        {props.options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </label>
  )
}

function ProfileCard(props: {
  profile: LlmProfile
  active: boolean
  onSetActive: () => void
  onUpdate: (p: LlmProfile) => void
  onRemove: () => void
  onTest: () => Promise<void>
  testState: TestState
}) {
  const p = props.profile
  const providerOptions: { value: Provider; label: string }[] = [
    { value: 'openai', label: 'openai' },
    { value: 'openai_compatible', label: 'openai_compatible' },
    { value: 'anthropic_compatible', label: 'anthropic_compatible' },
  ]

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold">{p.label}</div>
          <div className="mt-1 text-xs text-zinc-600 dark:text-zinc-400">id: {p.id}</div>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={props.onSetActive}
            className={
              props.active
                ? 'rounded-md bg-emerald-600 px-3 py-2 text-xs font-medium text-white'
                : 'rounded-md border border-zinc-200 bg-white px-3 py-2 text-xs font-medium hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800'
            }
          >
            {props.active ? 'Active' : 'Set active'}
          </button>
          <button
            type="button"
            onClick={props.onRemove}
            className="rounded-md border border-rose-200 bg-rose-50 px-3 py-2 text-xs font-medium text-rose-900 hover:bg-rose-100 dark:border-rose-900/40 dark:bg-rose-950/30 dark:text-rose-200 dark:hover:bg-rose-950/50"
          >
            Remove
          </button>
        </div>
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-2">
        <TextField label="id" value={p.id} onChange={(v) => props.onUpdate({ ...p, id: v })} />
        <TextField
          label="label"
          value={p.label}
          onChange={(v) => props.onUpdate({ ...p, label: v })}
        />
        <SelectField
          label="provider"
          value={p.provider}
          options={providerOptions}
          onChange={(v) => props.onUpdate({ ...p, provider: v })}
        />
        <TextField
          label="model"
          value={p.model}
          onChange={(v) => props.onUpdate({ ...p, model: v })}
          placeholder="gpt-4o-mini"
        />
        <TextField
          label="base_url"
          value={p.base_url}
          onChange={(v) => props.onUpdate({ ...p, base_url: v })}
          placeholder="https://api.openai.com/v1"
        />
        <TextField
          label="api_key_env"
          value={p.api_key_env}
          onChange={(v) => props.onUpdate({ ...p, api_key_env: v })}
          placeholder="OPENAI_API_KEY"
          // NOTE: openai_compatible often points to local llama.cpp/ollama which doesn't need a key.
          // Keep the field visible (so users can still set it), but avoid making it feel required.
        />
      </div>

      <div className="mt-4 flex items-center justify-between gap-3">
        <div className="text-xs text-zinc-600 dark:text-zinc-400">
          Headers are supported in config.yaml but edited manually (secrets must be env refs).
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={props.onTest}
            disabled={props.testState.status === 'testing'}
            className="rounded-md border border-zinc-200 bg-white px-3 py-2 text-xs font-medium hover:bg-zinc-50 disabled:opacity-60 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800"
          >
            {props.testState.status === 'testing' ? 'Testing…' : 'Test'}
          </button>
          {props.testState.status === 'ok' ? (
            <div className="text-xs font-medium text-emerald-700 dark:text-emerald-300">OK</div>
          ) : null}
          {props.testState.status === 'error' ? (
            <div className="text-xs font-medium text-rose-700 dark:text-rose-300">
              {props.testState.message ?? 'Error'}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}

export default function ConfigPage() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [config, setConfig] = useState<IntentConfig | null>(null)
  const [dirty, setDirty] = useState(false)
  const [saving, setSaving] = useState(false)
  const [tests, setTests] = useState<Record<string, TestState>>({})

  const profiles = useMemo(() => config?.llms.profiles ?? [], [config])

  async function refresh() {
    setLoading(true)
    try {
      setError(null)
      const cfg = await getConfig()
      setConfig(cfg)
      setDirty(false)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'failed to load')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  function updateProfile(idx: number, next: LlmProfile) {
    if (!config) return
    const nextProfiles = [...config.llms.profiles]
    nextProfiles[idx] = next
    setConfig({ ...config, llms: { ...config.llms, profiles: nextProfiles } })
    setDirty(true)
  }

  function removeProfile(idx: number) {
    if (!config) return
    const nextProfiles = config.llms.profiles.filter((_, i) => i !== idx)
    let nextActive = config.llms.active
    if (!nextProfiles.find((p) => p.id === nextActive) && nextProfiles.length > 0) {
      nextActive = nextProfiles[0].id
    }
    setConfig({ ...config, llms: { active: nextActive, profiles: nextProfiles } })
    setDirty(true)
  }

  function addProfile() {
    if (!config) return
    const baseId = 'profile'
    let n = 1
    const existing = new Set(config.llms.profiles.map((p) => p.id))
    while (existing.has(`${baseId}_${n}`)) n++
    const id = `${baseId}_${n}`
    const next: LlmProfile = {
      id,
      label: `Profile ${n}`,
      provider: 'openai_compatible',
      base_url: 'http://localhost:11434/v1',
      model: 'llama',
      api_key_env: 'LOCAL_API_KEY',
      headers: {},
    }
    setConfig({ ...config, llms: { ...config.llms, profiles: [...config.llms.profiles, next] } })
    setDirty(true)
  }

  function setActive(id: string) {
    if (!config) return
    setConfig({ ...config, llms: { ...config.llms, active: id } })
    setDirty(true)
  }

  async function onSave() {
    if (!config) return
    setSaving(true)
    try {
      setError(null)
      const saved = await saveConfig(config)
      setConfig(saved)
      setDirty(false)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'failed to save')
    } finally {
      setSaving(false)
    }
  }

  async function onTest(profileId: string) {
    setTests((t) => ({ ...t, [profileId]: { status: 'testing' } }))
    try {
      // Send current (possibly-unsaved) config so backend tests the draft.
      const r = await testProfile(profileId, config ?? undefined)

      // Some providers (local llama.cpp/ollama) don't require an API key.
      const requiresApiKey = Boolean(r.checks?.requires_api_key ?? true)
      const ok = requiresApiKey ? Boolean(r.checks?.api_key_present) : true
      setTests((t) => ({
        ...t,
        [profileId]: ok
          ? { status: 'ok' }
          : { status: 'error', message: `Missing env: ${r.checks?.api_key_env ?? 'api_key_env'}` },
      }))
    } catch (e) {
      setTests((t) => ({
        ...t,
        [profileId]: { status: 'error', message: e instanceof Error ? e.message : 'failed' },
      }))
    }
  }

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-lg font-semibold">Config</h1>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              Manage LLM profiles stored in <code className="font-mono">intent/config.yaml</code>. Secrets
              are referenced by env var name and loaded from <code className="font-mono">intent/.env</code>.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={refresh}
              className="rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm shadow-sm hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800"
            >
              Reload
            </button>
            <button
              type="button"
              onClick={addProfile}
              disabled={!config}
              className="rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm shadow-sm hover:bg-zinc-50 disabled:opacity-60 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800"
            >
              Add profile
            </button>
            <button
              type="button"
              onClick={onSave}
              disabled={!dirty || saving || !config}
              className="rounded-md bg-zinc-900 px-3 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-zinc-800 disabled:opacity-60 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200"
            >
              {saving ? 'Saving…' : dirty ? 'Save' : 'Saved'}
            </button>
          </div>
        </div>

        {loading ? <div className="mt-3 text-sm text-zinc-500">Loading…</div> : null}
        {error ? (
          <div className="mt-3 rounded-md border border-rose-200 bg-rose-50 p-2 text-sm text-rose-900 dark:border-rose-900/40 dark:bg-rose-950/30 dark:text-rose-200">
            {error}
          </div>
        ) : null}
      </section>

      {config ? (
        <section className="grid gap-4 md:grid-cols-2">
          {profiles.map((p, idx) => (
            <ProfileCard
              // IMPORTANT: keep React keys stable while editing the profile id.
              key={`${idx}`}
              profile={p}
              active={config.llms.active === p.id}
              onSetActive={() => setActive(p.id)}
              onUpdate={(next) => updateProfile(idx, next)}
              onRemove={() => removeProfile(idx)}
              onTest={() => onTest(p.id)}
              testState={tests[p.id] ?? { status: 'idle' }}
            />
          ))}
        </section>
      ) : null}
    </div>
  )
}
