import { act } from 'react'
import { createRoot } from 'react-dom/client'
import { MemoryRouter } from 'react-router-dom'
import { expect, it, vi } from 'vitest'
import { XViewPage } from './XViewPage'
import { fetchXView } from './service'

vi.mock('./service', () => ({ fetchXView: vi.fn() }))
vi.mock('./AnalysisWorkspacePage', () => ({ Search: ({ onSearch }: { onSearch: (query: object) => void }) => <button onClick={() => onSearch({ project_id: 'p1', conditionValue: 'I', searchValue: '10.0.' })}>Search</button> }))
vi.mock('./XViewDetailDialog', () => ({ XViewDetailDialog: ({ query }: { query: { xview_uri?: string } }) => <div role="dialog">{query.xview_uri}</div> }))
vi.mock('echarts-for-react', () => ({ default: ({ option, onEvents }: { option: { tooltip: { show: boolean }; dataZoom?: unknown; series: Array<{ large: boolean; progressive: number }> }; onEvents: { brushEnd: (event: object) => void } }) => {
  expect(option.tooltip.show).toBe(false)
  expect(option.dataZoom).toBeUndefined()
  // A brush visual update must use a complete layout, not the last progressive chunk.
  for (const series of option.series) {
    expect(series.large).toBe(true)
    expect(series.progressive).toBe(0)
  }
  return <button onClick={() => onEvents.brushEnd({ areas: [{ coordRange: [[new Date(2026, 8, 22, 9).getTime(), new Date(2026, 8, 22, 10).getTime()], [10, 20]] }] })}>Select area</button>
} }))

it('toggles server URI filtering and passes the selected URI into the area popup', async () => {
  Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true })
  vi.mocked(fetchXView).mockResolvedValue({ uris: [{ uri: '/a', count: 3 }, { uri: '/b', count: 2 }], points: [], total_count: 5, displayed_count: 0, sampled: false, sample_stride: 1 })
  const host = document.createElement('div')
  document.body.append(host)
  const root = createRoot(host)
  try {
    await act(async () => root.render(<MemoryRouter initialEntries={['/x-view?project_id=p1']}><XViewPage /></MemoryRouter>))
    await act(async () => (host.querySelector('button') as HTMLButtonElement).click())
    const uri = (index: number) => host.querySelectorAll<HTMLButtonElement>('.xview-uri-item')[index]
    await act(async () => uri(0).click())
    expect(fetchXView).toHaveBeenLastCalledWith(expect.objectContaining({ xview_uri: '/a', conditionValue: 'I', searchValue: '10.0.' }), expect.any(AbortSignal))
    await act(async () => uri(1).click())
    expect(fetchXView).toHaveBeenLastCalledWith(expect.objectContaining({ xview_uri: '/b' }), expect.any(AbortSignal))
    await act(async () => (host.querySelector('.xview-chart button') as HTMLButtonElement).click())
    expect(host.querySelector('[role="dialog"]')?.textContent).toBe('/b')
    await act(async () => uri(1).click())
    expect(fetchXView).toHaveBeenLastCalledWith(expect.objectContaining({ xview_uri: undefined }), expect.any(AbortSignal))
    expect(host.querySelector('[role="dialog"]')).toBeNull()
  } finally { await act(async () => root.unmount()); host.remove() }
})
