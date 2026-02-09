import { NavLink, Route, Routes } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'
import JobDetailPage from './pages/JobDetailPage'
import ConfigPage from './pages/ConfigPage'
import SettingsPage from './pages/SettingsPage'
import ThemeToggle from './components/ThemeToggle'

function NavItem(props: { to: string; label: string }) {
  return (
    <NavLink
      to={props.to}
      className={({ isActive }: { isActive: boolean }) =>
        [
          'rounded-md px-3 py-2 text-sm font-medium transition',
          isActive
            ? 'bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900'
            : 'text-zinc-700 hover:bg-zinc-200 dark:text-zinc-200 dark:hover:bg-zinc-800',
        ].join(' ')
      }
    >
      {props.label}
    </NavLink>
  )
}

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-zinc-200 bg-zinc-50/80 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/70">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400" />
            <div>
              <div className="text-sm font-semibold leading-4">Agent UI</div>
              <div className="text-xs text-zinc-600 dark:text-zinc-400">
                local jobs + live traces
              </div>
            </div>
          </div>

          <nav className="flex items-center gap-1" aria-label="Primary">
            <NavItem to="/" label="Dashboard" />
            <NavItem to="/config" label="Config" />
            <NavItem to="/settings" label="Settings" />
          </nav>

          <div className="flex items-center gap-2">
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/jobs/:jobId" element={<JobDetailPage />} />
          <Route path="/config" element={<ConfigPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  )
}

