import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiRequest } from '@/lib/api/client'
export function RegisterPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const submit = async () => {
    try {
      await apiRequest({
        method: 'POST',
        url: '/rest-auth/registration/',
        data: { username, password },
      })
      setMessage('등록이 완료되었습니다. 로그인해 주세요.')
      setTimeout(() => navigate('/login'), 400)
    } catch {
      setMessage('등록에 실패했습니다. 입력값과 서버 상태를 확인하세요.')
    }
  }
  return (
    <section className="dense-card status-panel">
      <h1>회원 등록</h1>
      <label>
        Username
        <input value={username} onChange={(event) => setUsername(event.target.value)} />
      </label>
      <label>
        Password
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
      </label>
      {message && <p role="status">{message}</p>}
      <button disabled={!username || !password} onClick={() => void submit()}>
        등록
      </button>
    </section>
  )
}
