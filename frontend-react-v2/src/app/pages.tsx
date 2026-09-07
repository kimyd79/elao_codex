import type { ReactNode } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from './auth'

function StatusPage({
  title,
  detail,
  children,
}: {
  title: string
  detail: string
  children?: ReactNode
}) {
  return (
    <section className="dense-card status-panel">
      <h1>{title}</h1>
      <p className="muted">{detail}</p>
      {children}
    </section>
  )
}
export function LoginPage() {
  const { signIn } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  return (
    <section className="dense-card status-panel">
      <h1>로그인</h1>
      <p className="muted">React v2 실행 기반 인증 화면입니다.</p>
      <button
        onClick={() => {
          signIn('fixture-user')
          navigate((location.state as { from?: string } | null)?.from ?? '/initialization', {
            replace: true,
          })
        }}
      >
        Fixture 로그인
      </button>
    </section>
  )
}
export function LogoutPage() {
  const { signOut } = useAuth()
  signOut()
  return <Navigate to="/login" replace />
}
export function HomePage() {
  return (
    <StatusPage title="Easy Log Analyzer" detail="React v2 기반 화면입니다.">
      <Link to="/initialization">시작하기</Link>
    </StatusPage>
  )
}
export function InitializationPage() {
  return (
    <StatusPage title="Initialization" detail="Phase 2에서 기존 Init 단계와 탭을 이전합니다." />
  )
}
export function LookupPage() {
  return <StatusPage title="Lookup" detail="Phase 3에서 AG Grid와 서버 커서 조회를 연결합니다." />
}
export function AnalysisPage() {
  return <StatusPage title="Analysis" detail="Phase 4에서 ECharts와 서버 집계를 연결합니다." />
}
export function NotFoundPage() {
  return <StatusPage title="페이지를 찾을 수 없습니다" detail="요청한 경로가 없습니다." />
}
