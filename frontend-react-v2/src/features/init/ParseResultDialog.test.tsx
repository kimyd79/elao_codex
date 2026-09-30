import { act } from 'react'
import { createRoot } from 'react-dom/client'
import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { ParseResultDialog } from './ParseResultDialog'
import type { ParseResult } from './service'

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true })
let root: ReturnType<typeof createRoot>
const result: ParseResult = {
  status: 'COMPLETED', source_count: 664076, stored_count: 664075, parsed_count: 664075, rejected_count: 1,
  files: [{ logfile_id: 'f1', file_name: 'example.log', status: 'COMPLETED', parsed_count: 664075, stored_count: 664075, rejected_count: 1,
    failure_reasons: [{ error_code: 'invalid_nul', error_message: 'NUL byte', count: 1 }],
    failure_samples: [{ line_number: 583401, error_code: 'invalid_nul', error_message: 'NUL byte', raw_line_excerpt: '<script>sample</script> \\0', truncated: true }],
  }],
}
beforeEach(() => {
  Object.defineProperty(HTMLDialogElement.prototype, 'showModal', { configurable: true, value: function (this: HTMLDialogElement) { this.open = true } })
  Object.defineProperty(HTMLDialogElement.prototype, 'close', { configurable: true, value: function (this: HTMLDialogElement) { this.open = false } })
  root = createRoot(document.createElement('div'))
})
afterEach(async () => { await act(async () => root.unmount()); vi.restoreAllMocks() })
const button = (text: string) => [...document.querySelectorAll<HTMLButtonElement>('dialog button')].find((b) => b.textContent?.includes(text))!

it('shows failure ratio, reasons and escaped log samples; staying does not load data', async () => {
  const onClose = vi.fn(), onContinue = vi.fn()
  await act(async () => root.render(<ParseResultDialog result={result} onClose={onClose} onContinue={onContinue} />))
  expect(document.querySelector('dialog')!.textContent).toContain('664,076')
  expect(document.querySelector('dialog')!.textContent).toContain('0.000151%')
  expect(document.querySelector('pre')!.textContent).toContain('<script>sample</script>')
  expect(document.querySelector('dialog script')).toBeNull()
  await act(async () => button('현재 단계').click())
  expect(onClose).toHaveBeenCalledOnce()
  expect(onContinue).not.toHaveBeenCalled()
})

it('starts loading only on continue, blocks duplicate clicks and allows retry after failure', async () => {
  let reject!: (error: Error) => void
  const onContinue = vi.fn((progress: (text: string) => void) => {
    progress('분석 데이터 로딩 중… 1/17')
    return new Promise<void>((_, fail) => { reject = fail })
  })
  await act(async () => root.render(<ParseResultDialog result={result} onClose={vi.fn()} onContinue={onContinue} />))
  expect(onContinue).not.toHaveBeenCalled()
  await act(async () => button('다음 단계').click())
  expect(button('현재 단계').disabled).toBe(true)
  expect(document.querySelector('[role="status"]')?.textContent).toContain('1/17')
  await act(async () => reject(new Error('offline')))
  expect(document.querySelector('[role="alert"]')?.textContent).toContain('offline')
  expect(button('다음 단계').disabled).toBe(false)
  expect(onContinue).toHaveBeenCalledOnce()
})

it('prevents advancing when parsing failed', async () => {
  await act(async () => root.render(<ParseResultDialog result={{ ...result, status: 'FAILED', stored_count: 0 }} onClose={vi.fn()} onContinue={vi.fn()} />))
  expect(button('다음 단계').disabled).toBe(true)
  expect(button('현재 단계').disabled).toBe(false)
})
