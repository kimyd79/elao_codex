import { Link } from 'react-router-dom'
export function ManagementPage() {
  return (
    <section className="dense-card">
      <h1>Management</h1>
      <p className="muted">프로젝트·로그 포맷·메트릭 관리 화면 진입점입니다.</p>
      <nav style={{ display: 'flex', gap: 12 }}>
        <Link to="/project">Project</Link>
        <Link to="/logformat">Log Format</Link>
        <Link to="/metrics">Metrics</Link>
      </nav>
    </section>
  )
}
