import { Link, useLocation } from 'react-router-dom'
export type DenseTab = { key: string; label: string; to: string; disabled?: boolean }
export function DenseTabs({ tabs }: { tabs: DenseTab[] }) {
  const location = useLocation()
  return (
    <div
      role="tablist"
      aria-label="화면 탭"
      style={{ display: 'flex', gap: 4, borderBottom: '1px solid #ddd6ee', marginBottom: 16 }}
    >
      {tabs.map((tab) => {
        const activeStep = new URLSearchParams(location.search).get('step') ?? 'project'
        const active =
          location.pathname === '/initialization'
            ? activeStep === tab.key
            : `${location.pathname}${location.search}` === tab.to
        return (
          <Link
            key={tab.key}
            role="tab"
            aria-selected={active}
            aria-disabled={tab.disabled}
            to={tab.disabled ? location.pathname : tab.to}
            style={{
              padding: '8px 14px',
              borderBottom: active ? '3px solid #5269d4' : '3px solid transparent',
              color: active ? '#30469f' : '#69758c',
              fontWeight: active ? 700 : 500,
              transition: 'all .2s ease',
              textDecoration: 'none',
              fontSize: 13,
            }}
          >
            {tab.label}
          </Link>
        )
      })}
    </div>
  )
}
