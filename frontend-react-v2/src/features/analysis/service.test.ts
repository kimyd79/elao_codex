import { describe, expect, it } from 'vitest'
import { toAnalysisRequest } from './service'

describe('analysis request contract', () => {
  it('keeps project/type at the top level and nests filters', () => {
    expect(toAnalysisRequest({ project_id: 'p1', type: '2', status: 500 })).toEqual({
      project_id: 'p1',
      type: '2',
      kind: 1,
      filter: { status: 500, project_id: 'p1' },
    })
  })
})
