import { describe, expect, it } from 'vitest'
import { ApiError } from './errors'

describe('ApiError', () => {
  it('normalizes backend payloads', () => {
    const error = new ApiError(400, { code: 'validation_error', detail: 'invalid' })
    expect(error.status).toBe(400)
    expect(error.code).toBe('validation_error')
    expect(error.message).toBe('invalid')
  })
})
