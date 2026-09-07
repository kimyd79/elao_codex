export type ApiErrorPayload = {
  code?: string
  detail?: string
  message?: string
  fields?: Record<string, string[]>
}

export class ApiError extends Error {
  readonly status: number
  readonly code?: string
  readonly fields?: Record<string, string[]>

  constructor(status: number, payload?: ApiErrorPayload, message = 'API 요청에 실패했습니다.') {
    super(payload?.message ?? payload?.detail ?? message)
    this.name = 'ApiError'
    this.status = status
    this.code = payload?.code
    this.fields = payload?.fields
  }
}
