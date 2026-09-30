import { beforeEach, expect, it, vi } from 'vitest'
import { apiRequest } from '@/lib/api/client'
import { fetchLogs } from './service'

vi.mock('@/lib/api/client', () => ({ apiRequest: vi.fn() }))

beforeEach(() => vi.resetAllMocks())

it('adds a statistics drill-down condition without dropping the active search filters', async () => {
  vi.mocked(apiRequest).mockResolvedValue({ results: [], count: 0 })
  await fetchLogs({
    projectId: 'p1',
    condition: 'I',
    search: '10.0.',
    excludeSearch: true,
    detailCondition: 'R',
    detailSearch: 'GET /health HTTP/1.1',
    server: 'web-01',
  })

  expect(apiRequest).toHaveBeenCalledWith(expect.objectContaining({
    method: 'GET',
    url: '/logdetail_dynamic/',
    params: expect.objectContaining({
      project_id: 'p1',
      conditionValue: 'I',
      searchValue: '10.0.',
      excludeSearch: true,
      detailconditionValue: 'R',
      detailsearchValue: 'GET /health HTTP/1.1',
      projectServers: 'web-01',
    }),
  }))
})

it('omits the None condition so a plain keyword remains a raw-log search', async () => {
  vi.mocked(apiRequest).mockResolvedValue({ results: [], count: 0 })
  await fetchLogs({ projectId: 'p1', condition: 'N', search: 'timeout' })
  const config = vi.mocked(apiRequest).mock.calls[0][0]
  expect(config.params).toHaveProperty('conditionValue', undefined)
  expect(config.params).toHaveProperty('searchValue', 'timeout')
})
