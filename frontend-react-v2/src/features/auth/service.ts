import { apiRequest } from '@/lib/api/client'
type LoginResponse = { key?: string; token?: string; user?: { username?: string; name?: string } }
export async function login(username: string, password: string) {
  const response = await apiRequest<LoginResponse>({
    method: 'POST',
    url: '/rest-auth/login/',
    data: { username, password },
  })
  return {
    token: response.key ?? response.token ?? '',
    userName: response.user?.username ?? response.user?.name ?? username,
  }
}
export async function logout() {
  return apiRequest<void>({ method: 'POST', url: '/rest-auth/logout/' })
}
