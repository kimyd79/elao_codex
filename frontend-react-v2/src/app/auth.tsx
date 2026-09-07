import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { logout as logoutApi } from '@/features/auth/service'
import { tokenKey } from './auth-token'

type AuthContextValue = {
  userName: string | null
  isAuthenticated: boolean
  signIn: (name: string, token?: string) => void
  signOut: () => void
}
const AuthContext = createContext<AuthContextValue | null>(null)
const key = 'elao-react-v2-auth'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [userName, setUserName] = useState<string | null>(() => sessionStorage.getItem(key))
  useEffect(() => {
    const expire = () => {
      sessionStorage.removeItem(key)
      setUserName(null)
    }
    window.addEventListener('elao:auth-expired', expire)
    return () => window.removeEventListener('elao:auth-expired', expire)
  }, [])
  const value = useMemo(
    () => ({
      userName,
      isAuthenticated: Boolean(userName),
      signIn: (name: string, token?: string) => {
        sessionStorage.setItem(key, name)
        if (token) sessionStorage.setItem(tokenKey, token)
        setUserName(name)
      },
      signOut: () => {
        sessionStorage.removeItem(key)
        sessionStorage.removeItem(tokenKey)
        setUserName(null)
        void logoutApi().catch(() => undefined)
      },
    }),
    [userName],
  )
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const value = useContext(AuthContext)
  if (!value) throw new Error('useAuth must be used within AuthProvider')
  return value
}
