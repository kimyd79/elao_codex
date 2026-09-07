import axios, { type AxiosError, type AxiosRequestConfig } from 'axios'
import { ApiError, type ApiErrorPayload } from './errors'
import { tokenKey } from '@/app/auth-token'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000/mwla',
  timeout: 30_000,
  headers: { Accept: 'application/json' },
  // The backend uses DRF TokenAuthentication. Disabling cookies keeps the
  // client compatible with the development API's wildcard CORS response.
  withCredentials: false,
})

apiClient.interceptors.request.use((config) => {
  const token = sessionStorage.getItem(tokenKey)
  if (token) config.headers.set('Authorization', `Token ${token}`)
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorPayload>) => {
    if (error.code === 'ERR_CANCELED') return Promise.reject(error)
    const status = error.response?.status ?? 0
    if (status === 401) window.dispatchEvent(new CustomEvent('elao:auth-expired'))
    return Promise.reject(new ApiError(status, error.response?.data, error.message))
  },
)

export async function apiRequest<T>(config: AxiosRequestConfig): Promise<T> {
  const response = await apiClient.request<T>(config)
  return response.data
}
