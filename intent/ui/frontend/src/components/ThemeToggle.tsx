import { useTheme } from '../state/theme'

export default function ThemeToggle() {
  const { theme, toggle } = useTheme()
  return (
    <button
      type="button"
      onClick={toggle}
      className="rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-800 shadow-sm transition hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-100 dark:hover:bg-zinc-800"
      aria-label="Toggle theme"
      title="Toggle theme"
    >
      {theme === 'dark' ? 'Dark' : 'Light'}
    </button>
  )
}
