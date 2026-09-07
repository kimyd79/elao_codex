import { describe, expect, it } from 'vitest'
import { createBenchmarkRows } from './benchmark'
describe('lookup benchmark fixture', () => {
  it('creates deterministic large row sets', () => {
    const rows = createBenchmarkRows(100_000)
    expect(rows).toHaveLength(100_000)
    expect(rows[0].line_no).toBe(1)
    expect(rows[99_999].line_no).toBe(100_000)
  })
})
