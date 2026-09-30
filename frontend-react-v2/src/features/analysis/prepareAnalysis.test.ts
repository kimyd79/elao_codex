import { beforeEach, expect, it, vi } from 'vitest'
import { apiRequest } from '@/lib/api/client'
import { listLogFiles, listProjects } from '@/features/init/service'
import { fetchChartData, fetchPeriod, fetchStatistics } from './service'
import { clearPreparedAnalysis, prepareAnalysis, takePreparedAnalysis } from './prepareAnalysis'

vi.mock('@/lib/api/client', () => ({ apiRequest: vi.fn() }))
vi.mock('@/features/init/service', () => ({ listLogFiles: vi.fn(), listProjects: vi.fn() }))
vi.mock('./service', () => ({ fetchChartData: vi.fn(), fetchPeriod: vi.fn(), fetchStatistics: vi.fn() }))
beforeEach(() => {
  vi.resetAllMocks()
  clearPreparedAnalysis()
  vi.mocked(listProjects).mockResolvedValue({ results: [{ project_id: 'p1', project_name: 'Test' }] })
  vi.mocked(listLogFiles).mockResolvedValue({ results: [{ logfile_id: 'f1', server_name: 'server', instance_name: 'instance' }] })
  vi.mocked(fetchPeriod).mockResolvedValue({ start_date: '20260101', end_date: '20260101', start_time: '010203', end_time: '020304' })
  vi.mocked(apiRequest).mockResolvedValue({ results: [{ result_count: 10 }] })
  vi.mocked(fetchChartData).mockResolvedValue({ resultX: ['20260101010203'], resultY: [1] })
  vi.mocked(fetchStatistics).mockImplementation(async (query) => ({
    results: [{ result: 'ok', result_count: 5 }],
    totalCnt: query.type === 8 ? 20 : 10,
  }))
})

it('preloads charts and all statistics before making the workspace ready', async () => {
  const progress = vi.fn()
  const result = await prepareAnalysis('p1', progress)
  expect(fetchChartData).toHaveBeenCalledTimes(3)
  expect(fetchStatistics).toHaveBeenCalledTimes(14)
  expect(fetchStatistics).toHaveBeenCalledWith(
    expect.objectContaining({ include_total: false }),
  )
  expect(result.query.projectServers).toEqual(['server-instance'])
  expect(result.statistics[1][0].result_per).toBe(50)
  expect(result.statistics[8][0].result_per).toBe(25)
  expect(result.statistics[4][0].result_per).toBeUndefined()
  expect(result.total).toBe(10)
  expect(takePreparedAnalysis('p1')).toBe(result)
  expect(takePreparedAnalysis('p2')).toBeUndefined()
  expect(progress).toHaveBeenLastCalledWith('분석 데이터 로딩 중… 17/17')
})

it('does not expose incomplete data when loading fails and supports retry', async () => {
  vi.mocked(fetchStatistics).mockRejectedValueOnce(new Error('offline'))
  await expect(prepareAnalysis('p1', vi.fn())).rejects.toThrow('offline')
  expect(takePreparedAnalysis('p1')).toBeUndefined()
  await expect(prepareAnalysis('p1', vi.fn())).resolves.toMatchObject({ projectId: 'p1' })
})
