import { describe, expect, it } from 'vitest'
import { featureFlags } from './flags'

describe('cutover feature flags', () => {
  it('defaults React v2 on and keeps a Vue fallback path', () => {
    expect(featureFlags.reactV2Enabled).toBe(true)
    expect(featureFlags.vueFallbackUrl).toBe('/mwla/')
  })
})
