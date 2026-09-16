import { Link, useLocation } from 'react-router-dom'
import type { CSSProperties } from 'react'
export type DenseTab = { key: string; label: string; to: string; disabled?: boolean }
export function DenseTabs({ tabs, activeKey, readOnly = false }: { tabs: DenseTab[]; activeKey?: string; readOnly?: boolean }) {
  const location = useLocation()
  return (
    <div
      role={readOnly ? 'list' : 'tablist'}
      aria-label={readOnly ? '진행 단계' : '화면 탭'}
      style={{ display: 'flex', gap: 4, borderBottom: '1px solid #ddd6ee', marginBottom: 16 }}
    >
      {tabs.map((tab) => {
        const activeStep = new URLSearchParams(location.search).get('step') ?? tabs[0]?.key
        const active =
          activeKey !== undefined ? activeKey === tab.key : location.pathname === '/initialization'
            ? activeStep === tab.key
            : `${location.pathname}${location.search}` === tab.to
        const style: CSSProperties = {
          padding: '8px 14px',
          borderBottom: active ? '3px solid #5269d4' : '3px solid transparent',
          color: active ? '#30469f' : '#69758c',
          fontWeight: active ? 700 : 500,
          transition: 'all .2s ease',
          textDecoration: 'none',
          fontSize: 13,
        }
        if (readOnly) return (
          <span key={tab.key} role="listitem" aria-current={active ? 'step' : undefined} style={{ ...style, cursor: 'default' }}>
            {tab.label}
          </span>
        )
        return (
          <Link
            key={tab.key}
            role="tab"
            aria-selected={active}
            aria-disabled={tab.disabled}
            to={tab.disabled ? location.pathname : tab.to}
            style={style}
          >
            {tab.label}
          </Link>
        )
      })}
    </div>
  )
}
