import { describe, expect, it, vi } from 'vitest'
import { apiRequest } from '@/lib/api/client'
import { fetchStatistics, fetchXView, toAnalysisRequest, toStatisticsRequest } from './service'

vi.mock('@/lib/api/client', () => ({ apiRequest: vi.fn() }))

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
    expect(request.include_total).toBe(true)
    expect(request.filter).not.toHaveProperty('N')
    expect(request.filter).not.toHaveProperty('include_total')
    expect(request.filter).toMatchObject({
      dateFromValue: '',
      timeFromValue: '',
      searchValue: '',
      project_id: 'p1',
    })
  })
  it('can skip duplicate total-count scans for a statistics request', () => {
    const request = toStatisticsRequest({ project_id: 'p1', type: 5, include_total: false })
    expect(request.include_total).toBe(false)
    expect(request.filter).not.toHaveProperty('include_total')
  })
  it('allows large statistics aggregations more time than ordinary API calls', async () => {
    vi.mocked(apiRequest).mockResolvedValue({ results: [] })
    await fetchStatistics({ project_id: 'p1', type: 2, N: 5 })
    expect(apiRequest).toHaveBeenCalledWith(expect.objectContaining({
      url: '/logdetail_dynamic/statistics/',
      timeout: 120_000,
    }))
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
  it('sends X-View filters to its request-level chart endpoint', async () => {
    vi.mocked(apiRequest).mockResolvedValue({ uris: [], points: [], total_count: 0, displayed_count: 0, sampled: false, sample_stride: 1 })
    await fetchXView({ project_id: 'p1', conditionValue: 'I', searchValue: '10.0.', projectServers: ['s1-i1'] })
    expect(apiRequest).toHaveBeenCalledWith(expect.objectContaining({
      method: 'POST',
      url: '/logdetail_dynamic/xview/',
      data: expect.objectContaining({
        project_id: 'p1',
        filter: expect.objectContaining({ conditionValue: 'I', searchValue: '10.0.', projectServers: ['s1-i1'] }),
      }),
    }))
  })
})
