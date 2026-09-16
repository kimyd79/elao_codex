import { act } from 'react'
import { createRoot } from 'react-dom/client'
import { expect, it, vi } from 'vitest'
import { ParsingProgress } from './ParsingProgress'
import { listAnalysisJobs } from './service'

vi.mock('./service', () => ({ listAnalysisJobs: vi.fn() }))

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true })

it('polls the current run, shows actual stage progress and retries failed status requests', async () => {
  vi.useFakeTimers()
  const host = document.createElement('div')
  const root = createRoot(host)
  const job = { job_id: 'job', status: 'PROCESSING', phase: 'VALIDATING', processed_units: 42, total_units: 100, progress_unit: 'bytes' }
  vi.mocked(listAnalysisJobs).mockResolvedValue([job])
  try {
    await act(async () => root.render(<ParsingProgress projectId="project" runId="run" />))
    expect(listAnalysisJobs).toHaveBeenCalledWith('project', 'run', expect.any(AbortSignal))
    expect(host.querySelector('[role="progressbar"]')?.getAttribute('aria-valuenow')).toBe('42')
    vi.mocked(listAnalysisJobs).mockRejectedValueOnce(new Error('network'))
    await act(async () => vi.advanceTimersByTime(1000))
    expect(host.textContent).toContain('temporarily unavailable')
    expect(host.querySelector('[role="progressbar"]')?.hasAttribute('aria-valuenow')).toBe(false)
    vi.mocked(listAnalysisJobs).mockResolvedValue([{ ...job, status: 'COMPLETED' }])
    await act(async () => vi.advanceTimersByTime(1000))
    expect(host.textContent).toContain('Files completed: 1 / 1')
    expect(host.textContent).toContain('Finalizing')
  } finally {
    await act(async () => root.unmount())
    expect(vi.getTimerCount()).toBe(0)
    vi.useRealTimers()
    vi.resetAllMocks()
  }
})

it('shows indeterminate progress and elapsed time, and cleans up on completion', async () => {
  vi.useFakeTimers()
  const host = document.createElement('div')
  const root = createRoot(host)
  try {
    await act(async () => root.render(<ParsingProgress />))
    const bar = host.querySelector('[role="progressbar"]')!
    expect(bar).not.toBeNull()
    expect(bar.hasAttribute('aria-valuenow')).toBe(false)
    expect(host.textContent).toContain('0:00 elapsed')
    await act(async () => vi.advanceTimersByTime(65000))
    expect(host.textContent).toContain('1:05 elapsed')
    await act(async () => root.render(null))
    expect(host.querySelector('[role="progressbar"]')).toBeNull()
    expect(vi.getTimerCount()).toBe(0)
    await act(async () => root.render(<ParsingProgress />))
    expect(host.textContent).toContain('0:00 elapsed')
  } finally {
    await act(async () => root.unmount())
    vi.useRealTimers()
  }
})
