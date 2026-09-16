import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { login } from './service'
import { useAuth } from '@/app/auth'

export function LoginApiPage() {
  const { signIn } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)
  const destination = (location.state as { from?: string } | null)?.from ?? '/initialization'
  const submit = async () => {
    setPending(true)
    setError('')
    try {
      const result = await login(username, password)
      signIn(result.userName, result.token)
      navigate(destination, { replace: true })
    } catch (error) {
      const detail = error instanceof Error ? error.message : 'Unknown error'
      setError(`Login failed (${detail}). Check the API connection or credentials.`)
    } finally {
      setPending(false)
    }
  }
  return (
    <section className="dense-card status-panel auth-page">
      <div className="auth-hero">
        <div className="auth-kicker">Easy Log Analyzer · v2</div>
        <h1>Turn raw logs into clear decisions.</h1>
        <p>Explore millions of events with fast, focused analysis.</p>
        <div className="auth-points">
          <span>Cursor-based log browsing</span>
          <span>Server-side aggregation</span>
          <span>Dense, responsive workspace</span>
        </div>
      </div>
      <div className="auth-form">
        <h2>Welcome back</h2>
        <p className="muted">Sign in to continue to your workspace.</p>
        <label>
          Username
          <input
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoComplete="username"
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
          />
        </label>
        {error && <p role="alert">{error}</p>}
        <button disabled={pending || !username || !password} onClick={() => void submit()}>
          Sign in
        </button>
        <div className="auth-divider">CREATE ACCOUNT</div>
        <button type="button" onClick={() => navigate('/register')}>회원가입</button>
        <div className="auth-divider">LOCAL PREVIEW</div>
        <button
          onClick={() => {
            signIn('fixture-user')
            navigate(destination, { replace: true })
          }}
        >
          Continue with fixture
        </button>
      </div>
    </section>
  )
}
