import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { apiClient } from '@/lib/api/client'

export function RegisterPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)
  const [done, setDone] = useState(false)
  const submit = async (event: FormEvent) => {
    event.preventDefault()
    if (pending) return
    setError('')
    if (password !== confirm) { setError('비밀번호와 비밀번호 확인이 일치하지 않습니다.'); return }
    setPending(true)
    try {
      await axios.post(`${apiClient.defaults.baseURL}/rest-auth/registration/`, {
        username: username.trim(), email: email.trim(), password1: password, password2: confirm,
      }, { timeout: 30000 })
      setDone(true)
      setPassword(''); setConfirm('')
    } catch (reason) {
      const data = axios.isAxiosError(reason) ? reason.response?.data : null
      setError(data && typeof data === 'object' ? Object.values(data).flat().map(String).join(' ') : '회원가입에 실패했습니다. 서버 연결을 확인해주세요.')
    } finally { setPending(false) }
  }
  return (
    <section className="dense-card status-panel auth-page">
      <div className="auth-hero"><div className="auth-kicker">Easy Log Analyzer</div><h1>Create your account.</h1><p>로그 분석을 시작할 계정을 등록하세요.</p></div>
      <form className="auth-form" onSubmit={(event) => void submit(event)}>
        <h2>회원가입</h2>
        {done ? <p role="status">회원가입이 완료되었습니다. 로그인해주세요.</p> : <>
          <label>Username<input required maxLength={150} autoComplete="username" value={username} disabled={pending} onChange={(event) => setUsername(event.target.value)} /></label>
          <label>비밀번호<input required type="password" autoComplete="new-password" value={password} disabled={pending} onChange={(event) => setPassword(event.target.value)} /></label>
          <label>비밀번호 확인<input required type="password" autoComplete="new-password" value={confirm} disabled={pending} onChange={(event) => setConfirm(event.target.value)} /></label>
          <label>이메일<input required type="email" autoComplete="email" value={email} disabled={pending} onChange={(event) => setEmail(event.target.value)} /></label>
          {error && <div className="auth-error-notice" role="alert">
            <span className="auth-error-icon" aria-hidden="true">!</span>
            <div><strong>입력 내용을 확인해주세요</strong><p>{error}</p></div>
          </div>}
          <button type="submit" disabled={pending}>{pending ? '가입 중...' : '회원가입'}</button>
        </>}
        <div className="auth-divider">SIGN IN</div>
        <button type="button" disabled={pending} onClick={() => navigate('/login')}>로그인으로 돌아가기</button>
      </form>
    </section>
  )
}
