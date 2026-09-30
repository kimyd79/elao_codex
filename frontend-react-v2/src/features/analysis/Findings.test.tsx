import { act } from 'react'
import { createRoot } from 'react-dom/client'
import { afterEach, expect, it, vi } from 'vitest'
import { apiRequest } from '@/lib/api/client'
import { Findings, type FindingsResult } from './Findings'

vi.mock('@/lib/api/client', () => ({ apiRequest: vi.fn() }))
Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true })
let root: ReturnType<typeof createRoot>
const host = document.createElement('div')
const result: FindingsResult = { total: 10, scope: { start: '2026-01-01', end: '2026-01-02', bucket_seconds: 60 },
  findings: [{ id: 'server_errors', title: '서버 오류 증가', status: 'detected', rule: '5xx 분석',
    evidence: { count: 2, top_urls: [{ frequest: 'GET /broken', count: 2 }] }, guidance: ['배포 이력 확인'] }], limitations: ['후보입니다.'] }
afterEach(async () => { await act(async () => root.unmount()); host.remove(); vi.clearAllMocks() })
async function render() {
  document.body.append(host); root = createRoot(host)
  await act(async () => root.render(<Findings projectId="p1" />))
}
it('renders findings, evidence and guidance and applies Search filters', async () => {
  vi.mocked(apiRequest).mockResolvedValue(result)
  await render()
  expect(host.textContent).toContain('서버 오류 증가')
  expect(host.textContent).toContain('GET /broken')
  expect(host.textContent).toContain('배포 이력 확인')
  expect(host.textContent).not.toContain('[object Object]')
  await act(async () => window.dispatchEvent(new CustomEvent('elao:analysis-search', {
    detail: { project_id: 'p1', conditionValue: 'S', searchValue: '500', projectServers: ['s-a'] },
  })))
  expect(apiRequest).toHaveBeenLastCalledWith(expect.objectContaining({ data: {
    project_id: 'p1', filter: { conditionValue: 'S', searchValue: '500', projectServers: ['s-a'] },
  } }))
})
it('discards stale responses after a filter change', async () => {
  let old!: (value: FindingsResult) => void
  vi.mocked(apiRequest).mockImplementationOnce(() => new Promise((resolve) => { old = resolve }))
    .mockResolvedValue({ ...result, total: 0, findings: [] })
  await render()
  expect(host.textContent).toContain('분석 중')
  await act(async () => window.dispatchEvent(new CustomEvent('elao:analysis-search', { detail: { project_id: 'p1', searchValue: 'new' } })))
  await act(async () => old(result))
  expect(host.textContent).toContain('선택 조건에 해당하는 로그가 없습니다')
  expect(host.textContent).not.toContain('GET /broken')
})
it('shows errors with retry instead of a clear finding', async () => {
  vi.mocked(apiRequest).mockRejectedValueOnce(new Error('failure')).mockResolvedValue(result)
  await render()
  expect(host.querySelector('[role="alert"]')).not.toBeNull()
  await act(async () => host.querySelector('button')!.click())
  expect(host.querySelector('[role="alert"]')).toBeNull()
  expect(host.textContent).toContain('확인 필요')
})
