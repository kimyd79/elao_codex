import { describe, expect, it } from 'vitest'
import { managementUrl } from './service'

describe('management API URLs', () => {
  it('builds collection and item URLs for every resource', () => {
    expect(managementUrl('project')).toBe('/logmaster/')
    expect(managementUrl('logformat', 'a/b')).toBe('/logformat/a%2Fb/')
    expect(managementUrl('metrics', 42)).toBe('/metrics/42/')
  })
})
