import { Link, Outlet } from 'react-router-dom'
import { useAuth } from './auth'
import { featureFlags } from '@/lib/flags'

export function AppShell() {
  const { userName, signOut } = useAuth()
  return (
    <div className="dense-shell">
      <header className="dense-header">
        <strong style={{ letterSpacing: '-0.02em', fontSize: 17 }}>
          {import.meta.env.VITE_APP_NAME ?? 'Easy Log Analyzer'}
        </strong>
        <nav style={{ marginLeft: 24, display: 'flex', gap: 12 }}>
          <Link to="/initialization" style={{ color: 'white' }}>
            Init
          </Link>
          <Link to="/lookup" style={{ color: 'white' }}>
            Lookup
          </Link>
          <Link to="/analysis" style={{ color: 'white' }}>
            Analysis
          </Link>
          <a href={featureFlags.vueFallbackUrl} style={{ color: 'white' }}>
            Vue fallback
          </a>
        </nav>
        <span style={{ marginLeft: 'auto' }}>
          {userName}
          <button onClick={signOut} style={{ marginLeft: 12 }}>
            Logout
          </button>
        </span>
      </header>
      <main className="dense-main">
        <Outlet />
      </main>
    </div>
  )
}
