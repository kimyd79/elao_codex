import { act } from 'react'
import { createRoot } from 'react-dom/client'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, expect, it, vi } from 'vitest'
import { AnalysisChartPage, StatisticsPage } from './AnalysisChartPage'
import { fetchChartData, fetchStatistics, type ChartPayload } from './service'
import { ApiError } from '@/lib/api/errors'

vi.mock('echarts-for-react', () => ({ default: () => null }))
vi.mock('./StatisticDetailDialog', () => ({
  StatisticDetailDialog: ({ selection }: { selection: { type: number; value: string } }) => <div role="dialog">{selection.type}:{selection.value}</div>,
}))
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

it('limits concurrent statistics requests to protect the database', async () => {
  let active = 0
  let maximum = 0
  const releases: Array<() => void> = []
  vi.mocked(fetchStatistics).mockImplementation(() => new Promise((resolve) => {
    active += 1
    maximum = Math.max(maximum, active)
    releases.push(() => {
      active -= 1
      resolve({ results: [], totalCnt: 0 })
    })
  }))
  document.body.append(host)
  window.history.replaceState({}, '', '/analysis?project_id=p1')
  root = createRoot(host)
  await act(async () => root.render(<MemoryRouter initialEntries={['/analysis?project_id=p1']}><StatisticsPage /></MemoryRouter>))

  expect(fetchStatistics).toHaveBeenCalledTimes(1)
  while (releases.length) {
    await act(async () => releases.shift()?.())
  }
  expect(fetchStatistics).toHaveBeenCalledTimes(14)
  expect(maximum).toBe(3)
  expect(fetchStatistics).toHaveBeenNthCalledWith(
    1,
    expect.objectContaining({ type: 1, include_total: true }),
    expect.any(AbortSignal),
  )
  expect(fetchStatistics).toHaveBeenNthCalledWith(
    2,
    expect.objectContaining({ include_total: false }),
    expect.any(AbortSignal),
  )
})

it('places comparison statistics progress beside the Retry button', async () => {
  vi.mocked(fetchStatistics).mockImplementation(() => new Promise(() => {}))
  document.body.append(host)
  root = createRoot(host)
  await act(async () =>
    root.render(
      <MemoryRouter initialEntries={['/analysis?project_id=p1']}>
        <StatisticsPage manual eventName="elao:comparison-statistic-1" />
      </MemoryRouter>,
    ),
  )

  await act(async () => {
    window.dispatchEvent(
      new CustomEvent('elao:comparison-statistic-1', { detail: { project_id: 'p1' } }),
    )
  })

  const controls = host.querySelector('.statistics-controls')
  expect(controls?.querySelector('button')?.textContent).toBe('조회 중…')
  expect(controls?.querySelector('[role="status"]')?.textContent).toContain('통계 조회 중')
  expect(host.querySelector('.statistics-workspace > .query-progress')).toBeNull()
})

it('renders statistic tables in the requested left-to-right pair order', async () => {
  vi.mocked(fetchStatistics).mockResolvedValue({ results: [], totalCnt: 0 })
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

  expect(Array.from(host.querySelectorAll('.statistic-table-title'), (title) => title.textContent)).toEqual([
    'Requests URI (count)',
    'Visitors (count)',
    'Requests Time-taken (s/㎲)',
    'Requests Average Time-taken (s/㎲)',
    'HTTP Status Codes (count)',
    '404 Requests URI (count)',
    'Requests URI (Total MB)',
    'Requests URI (Average MB)',
    'Referers (count)',
    'User Agent (count)',
    'Static file Names (count)',
    'Static files (count)',
    'Upstream Info (count)',
    'Domains (count, K8S Ingress)',
  ])
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
  expect(Array.from(select.options, (option) => option.value)).toEqual(['1', '5', '10', '20', '30'])
  await act(async () => {
    select.value = '30'
    select.dispatchEvent(new Event('change', { bubbles: true }))
  })
  expect(fetchStatistics).toHaveBeenLastCalledWith(
    expect.objectContaining({ N: 30 }),
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
    expect.objectContaining({ N: 30, projectServers: ['s2-i2'], searchValue: '/filtered' }),
    expect.any(AbortSignal),
  )
})

it('displays total and average byte statistics in MB', async () => {
  vi.mocked(fetchStatistics).mockImplementation(async (query) => ({
    results: [{
      result: '/download',
      result_count: query.type === 8 ? 1_572_864 : query.type === 10 ? 524_288 : 1,
    }],
    totalCnt: query.type === 8 ? 2_097_152 : 1,
  }))
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

  expect(host.textContent).toContain('Requests URI (Total MB)')
  expect(host.textContent).toContain('1.50 MB')
  expect(host.textContent).toContain('Requests URI (Average MB)')
  expect(host.textContent).toContain('0.50 MB')
  const totalMbTable = Array.from(host.querySelectorAll('.statistic-table-wrap')).find(
    (table) => table.querySelector('h3')?.textContent === 'Requests URI (Total MB)',
  )
  expect(totalMbTable?.textContent).toContain('75.00%')
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

it('opens the matching statistics detail when a result row is selected', async () => {
  vi.mocked(fetchStatistics).mockResolvedValue({ results: [{ result: '/orders', result_count: 4 }], totalCnt: 4 })
  document.body.append(host)
  window.history.replaceState({}, '', '/analysis?project_id=p1')
  root = createRoot(host)
  await act(async () => root.render(<MemoryRouter initialEntries={['/analysis?project_id=p1']}><StatisticsPage /></MemoryRouter>))

  await act(async () => (host.querySelector('.statistic-clickable-row') as HTMLElement).click())
  expect(host.querySelector('[role="dialog"]')?.textContent).toBe('2:/orders')
})
