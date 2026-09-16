import { act } from 'react'
import { createRoot } from 'react-dom/client'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, expect, it, vi } from 'vitest'
import { AnalysisChartPage, StatisticsPage } from './AnalysisChartPage'
import { fetchChartData, fetchStatistics, type ChartPayload } from './service'
import { ApiError } from '@/lib/api/errors'

vi.mock('echarts-for-react', () => ({ default: () => null }))
vi.mock('@/features/init/service', () => ({
  listLogFiles: vi
    .fn()
    .mockResolvedValue({ results: [{ server_name: 'server1', instance_name: 'instance1' }] }),
}))
vi.mock('./service', () => ({ fetchStatistics: vi.fn(), fetchChartData: vi.fn() }))
Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true })
const host = document.createElement('div')
let root: ReturnType<typeof createRoot>
afterEach(async () => {
  await act(async () => root.unmount())
  host.remove()
  vi.clearAllMocks()
  window.history.replaceState({}, '', '/')
})

it('shows pending statistics and clears indicators after the response', async () => {
  let finish!: (value: ChartPayload) => void
  vi.mocked(fetchStatistics).mockImplementation(() => new Promise((resolve) => { finish = resolve }))
  document.body.append(host)
  root = createRoot(host)
  await act(async () => root.render(<MemoryRouter initialEntries={['/analysis?project_id=p1']}><StatisticsPage /></MemoryRouter>))
  expect(host.querySelectorAll('[aria-busy="true"]')).toHaveLength(14)
  expect(host.textContent).toContain('데이터 조회 중')
  await act(async () => finish({ results: [{ result: '/loaded', result_count: 1 }], totalCnt: 1 }))
  expect(host.querySelectorAll('[aria-busy="true"]')).toHaveLength(13)
  expect(host.textContent).toContain('/loaded')
})

it('keeps chart loading for a newer search when an older response arrives', async () => {
  const responses: Array<(value: ChartPayload) => void> = []
  vi.mocked(fetchChartData).mockImplementation(() => new Promise((resolve) => responses.push(resolve)))
  vi.mocked(fetchStatistics).mockResolvedValue({ results: [] })
  document.body.append(host)
  root = createRoot(host)
  await act(async () => root.render(<MemoryRouter><AnalysisChartPage /></MemoryRouter>))
  const search = () => window.dispatchEvent(new CustomEvent('elao:analysis-search', { detail: { project_id: 'p1' } }))
  await act(async () => { search() })
  expect(host.querySelectorAll('[aria-busy="true"]')).toHaveLength(3)
  await act(async () => { search() })
  await act(async () => responses[0]({ resultX: [], resultY: [] }))
  expect(host.querySelectorAll('[aria-busy="true"]')).toHaveLength(3)
  await act(async () => { responses.slice(3).forEach((finish) => finish({ resultX: [], resultY: [] })) })
  expect(host.querySelectorAll('[aria-busy="true"]')).toHaveLength(0)
  expect(host.textContent).toContain('차트 조회 완료')
})

it('loads on entry, respects Top N, and refreshes with Search filters', async () => {
  vi.mocked(fetchStatistics).mockResolvedValue({
    results: [{ result: '/actual-log', result_count: 7 }],
    totalCnt: 10,
  })
  document.body.append(host)
  window.history.replaceState({}, '', '/analysis?project_id=p1')
  root = createRoot(host)
  await act(async () =>
    root.render(
      <MemoryRouter initialEntries={['/analysis?project_id=p1']}>
        <StatisticsPage />
      </MemoryRouter>,
    ),
  )
  expect(fetchStatistics).toHaveBeenCalledTimes(14)
  expect(fetchStatistics).toHaveBeenCalledWith(
    expect.objectContaining({ project_id: 'p1', projectServers: ['server1-instance1'], N: 5 }),
    expect.any(AbortSignal),
  )
  expect(host.textContent).toContain('/actual-log')
  expect(host.textContent).toContain('70.00%')
  const select = host.querySelector('select')!
  await act(async () => {
    select.value = '10'
    select.dispatchEvent(new Event('change', { bubbles: true }))
  })
  expect(fetchStatistics).toHaveBeenLastCalledWith(
    expect.objectContaining({ N: 10 }),
    expect.any(AbortSignal),
  )
  await act(async () => {
    window.dispatchEvent(
      new CustomEvent('elao:analysis-search', {
        detail: { project_id: 'p1', projectServers: ['s2-i2'], searchValue: '/filtered' },
      }),
    )
  })
  expect(fetchStatistics).toHaveBeenLastCalledWith(
    expect.objectContaining({ N: 10, projectServers: ['s2-i2'], searchValue: '/filtered' }),
    expect.any(AbortSignal),
  )
})

it('displays API failure rather than fabricated zero rows', async () => {
  vi.mocked(fetchStatistics).mockRejectedValue(new ApiError(500, { message: 'failed' }))
  document.body.append(host)
  window.history.replaceState({}, '', '/analysis?project_id=p1')
  root = createRoot(host)
  await act(async () =>
    root.render(
      <MemoryRouter initialEntries={['/analysis?project_id=p1']}>
        <StatisticsPage />
      </MemoryRouter>,
    ),
  )
  expect(host.textContent).toContain('Unable to load (HTTP 500)')
  expect(host.querySelector('tbody tr')?.children).toHaveLength(1)
})
