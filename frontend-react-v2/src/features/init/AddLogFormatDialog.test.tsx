import { act } from 'react'
import { createRoot } from 'react-dom/client'
import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { AddLogFormatDialog } from './AddLogFormatDialog'
import { createLogFormat, listLogFormatKinds } from './service'

vi.mock('./service', () => ({ createLogFormat: vi.fn(), listLogFormatKinds: vi.fn() }))
Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true })
const host = document.createElement('div')
let root: ReturnType<typeof createRoot>
beforeEach(() => {
  vi.resetAllMocks()
  Object.defineProperty(HTMLDialogElement.prototype, 'showModal', { configurable: true, value: function (this: HTMLDialogElement) { this.open = true } })
  Object.defineProperty(HTMLDialogElement.prototype, 'close', { configurable: true, value: function (this: HTMLDialogElement) { this.open = false } })
  vi.mocked(listLogFormatKinds).mockResolvedValue({ list_format_kind: ['apache', 'nginx'] })
  root = createRoot(host)
})
afterEach(async () => { await act(async () => root.unmount()); vi.restoreAllMocks() })

it('loads original format kinds and saves required values with the logged-in creator', async () => {
  const onSaved = vi.fn()
  const result = { format_id: 'new-id', format_kind: 'apache', format_name: 'custom', format_strings: '%h %r / %s' }
  vi.mocked(createLogFormat).mockResolvedValue(result)
  await act(async () => root.render(<AddLogFormatDialog creator="admin" onClose={vi.fn()} onSaved={onSaved} />))
  const dialog = document.querySelector('dialog')!
  expect(dialog.open).toBe(true)
  expect(dialog.querySelector('button[type="submit"]')?.hasAttribute('disabled')).toBe(true)
  const select = dialog.querySelector('select')!
  await act(async () => { select.value = 'apache'; select.dispatchEvent(new Event('change', { bubbles: true })) })
  const input = dialog.querySelector('input:not([readonly])')!
  const textarea = dialog.querySelector('textarea')!
  await act(async () => {
    Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value')!.set!.call(input, 'custom')
    input.dispatchEvent(new Event('input', { bubbles: true }))
    Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value')!.set!.call(textarea, '%h %r / %s')
    textarea.dispatchEvent(new Event('input', { bubbles: true }))
  })
  expect(dialog.querySelector('button[type="submit"]')?.hasAttribute('disabled')).toBe(false)
  await act(async () => { dialog.querySelector('form')!.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true })) })
  expect(createLogFormat).toHaveBeenCalledWith({ format_kind: 'apache', format_name: 'custom', format_strings: '%h %r / %s', creator: 'admin' })
  expect(onSaved).toHaveBeenCalledWith(result)
})

it('displays kind loading failure and allows closing without saving', async () => {
  vi.mocked(listLogFormatKinds).mockRejectedValue(new Error('offline'))
  const onClose = vi.fn()
  await act(async () => root.render(<AddLogFormatDialog creator="admin" onClose={onClose} onSaved={vi.fn()} />))
  expect(document.querySelector('[role="alert"]')?.textContent).toContain('불러오지 못했습니다')
  await act(async () => { document.querySelector<HTMLButtonElement>('[aria-label="Close log format dialog"]')!.click() })
  expect(onClose).toHaveBeenCalled()
  expect(createLogFormat).not.toHaveBeenCalled()
})
