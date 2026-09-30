import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from './auth'
import { featureFlags } from '@/lib/flags'

export function AppShell() {
  const { userName, signOut } = useAuth()
  const { pathname, search } = useLocation()
  return (
    <div className="dense-shell">
      <header className="dense-header">
        <strong className="app-brand">
          {import.meta.env.VITE_APP_NAME ?? 'Easy Log Analyzer'}
        </strong>
        <nav className="app-navigation" aria-label="Main navigation">
          <NavLink to="/initialization" className="app-nav-link">
            Initialization
          </NavLink>
          <NavLink to="/lookup" className="app-nav-link">
            Lookup
          </NavLink>
          <NavLink to={['/detail', '/analysis', '/x-view'].includes(pathname) ? `/analysis${search}` : '/analysis'} className="app-nav-link">
            Analysis
          </NavLink>
          <NavLink to={['/analysis', '/x-view'].includes(pathname) ? `/detail${search}` : '/detail'} className="app-nav-link">
            Detail
          </NavLink>
          <NavLink to={`/x-view${search}`} className="app-nav-link">X-View</NavLink>
          <NavLink to={`/comparison_chart${search}`} className="app-nav-link">Comparison-Chart</NavLink>
          <NavLink to={`/comparison_statistic${search}`} className="app-nav-link">Comparison-Statistic</NavLink>
        </nav>
        <div className="app-account">
          <a className="app-fallback-link" href={featureFlags.vueFallbackUrl}>Vue fallback</a>
          <span className="app-user-name">{userName}</span>
          <button className="app-logout" onClick={signOut}>
            Logout
          </button>
        </div>
      </header>
      <main className={`dense-main${['/analysis', '/detail', '/x-view', '/comparison_chart', '/comparison_statistic'].includes(pathname) ? ' dense-main-fluid' : ''}`}>
        <Outlet />
      </main>
    </div>
  )
}
