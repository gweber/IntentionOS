import { useTheme } from '../state/theme'

export default function SettingsPage() {
  const { theme, setTheme } = useTheme()
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900">
        <h1 className="text-lg font-semibold">Settings</h1>
        <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">Preferences are stored locally.</p>
      </div>

      <div className="rounded-2xl border border-zinc-200 bg-white p-4 shadow-card dark:border-zinc-800 dark:bg-zinc-900">
        <div className="text-sm font-semibold">Theme</div>
        <div className="mt-3 flex items-center gap-2">
          <button
            type="button"
            onClick={() => setTheme('light')}
            className={
              theme === 'light'
                ? 'rounded-md bg-zinc-900 px-3 py-2 text-sm text-white dark:bg-zinc-100 dark:text-zinc-900'
                : 'rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800'
            }
          >
            Light
          </button>
          <button
            type="button"
            onClick={() => setTheme('dark')}
            className={
              theme === 'dark'
                ? 'rounded-md bg-zinc-900 px-3 py-2 text-sm text-white dark:bg-zinc-100 dark:text-zinc-900'
                : 'rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:bg-zinc-800'
            }
          >
            Dark
          </button>
        </div>
      </div>
    </div>
  )
}
