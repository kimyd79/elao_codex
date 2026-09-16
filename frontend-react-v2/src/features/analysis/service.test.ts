import { describe, expect, it } from 'vitest'
import { toAnalysisRequest, toStatisticsRequest } from './service'

describe('analysis request contract', () => {
  it('keeps project/type at the top level and nests filters', () => {
    expect(toAnalysisRequest({ project_id: 'p1', type: '2', status: 500 })).toMatchObject({
      project_id: 'p1',
      type: '2',
      kind: 1,
      filter: { status: 500, project_id: 'p1' },
    })
  })
  it('sends the selected Top N and numeric statistics type at the top level', () => {
    const request = toStatisticsRequest({ project_id: 'p1', type: '2', N: 10 })
    expect(request.type).toBe(2)
    expect(request.N).toBe(10)
    expect(request.filter).not.toHaveProperty('N')
    expect(request.filter).toMatchObject({
      dateFromValue: '',
      timeFromValue: '',
      searchValue: '',
      project_id: 'p1',
    })
  })
  it('normalizes URL instance lists and false exclude flags', () => {
    const request = toStatisticsRequest({
      project_id: 'p1',
      projectServers: 's1-i1,s2-i2',
      excludeSearch: 'false',
    })
    expect(request.filter.projectServers).toEqual(['s1-i1', 's2-i2'])
    expect(request.filter.excludeSearch).toBe(false)
    expect(toAnalysisRequest({ projectServers: [], excludeSearch: 'true' }).filter).toMatchObject({
      projectServers: [],
      excludeSearch: true,
    })
  })
})
