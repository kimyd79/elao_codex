import { beforeEach, describe, expect, it, vi } from 'vitest'
import { apiRequest } from '@/lib/api/client'
import { deleteProject, parseProjectFiles, uploadLogFile } from './service'

vi.mock('@/lib/api/client', () => ({ apiRequest: vi.fn() }))
beforeEach(() => vi.resetAllMocks())
describe('legacy upload and parsing contract', () => {
  it('allows project deletion to wait for active database work', async () => {
    vi.mocked(apiRequest).mockResolvedValue(undefined)
    await deleteProject('p1')
    expect(apiRequest).toHaveBeenCalledWith({ method: 'DELETE', url: '/logmaster/p1/', timeout: 120_000 })
  })
  it('keeps slash characters in uploaded log formats', async () => {
    vi.mocked(apiRequest).mockResolvedValue({ logfile_id: 'f1' })
    await uploadLogFile('p1', new File(['log'], 'access.log'), 'nginx/main/$request / $status', 'server', 'instance')
    const data = vi.mocked(apiRequest).mock.calls[0][0].data as FormData
    expect(data.get('file_format')).toBe('$request / $status')
    expect(data.get('format_kind')).toBe('nginx')
    expect(data.get('format_name')).toBe('main')
  })
  it('waits for the original parsing endpoint and accepts previously stored files', async () => {
    const result = { status: 'COMPLETED', source_count: 10, parsed_count: 10, stored_count: 10, rejected_count: 0, files: [{ logfile_id: 'f1', status: 'ALREADY_COMPLETED', parsed_count: 10, stored_count: 10 }] }
    vi.mocked(apiRequest).mockResolvedValue(result)
    await expect(parseProjectFiles('p1', ['f1'])).resolves.toEqual(result)
    expect(apiRequest).toHaveBeenCalledWith(expect.objectContaining({ method: 'POST', url: '/logdetail_dynamic/', timeout: 0, data: { project_id: 'p1', logfile_id: ['f1'], diff_hour: 0 } }))
  })
  it('rejects missing files, partial parsing and inconsistent stored counts', async () => {
    await expect(parseProjectFiles('p1', [])).rejects.toThrow('at least one')
    expect(apiRequest).not.toHaveBeenCalled()
    for (const result of [
      { status: 'PARTIAL', parsed_count: 9, stored_count: 9, rejected_count: 1 },
      { status: 'COMPLETED', parsed_count: 10, stored_count: 0, rejected_count: 0 },
      { status: 'COMPLETED', parsed_count: 10, stored_count: 10, rejected_count: 0, files: [] },
    ]) {
      vi.mocked(apiRequest).mockResolvedValue(result)
      await expect(parseProjectFiles('p1', ['f1'])).rejects.toThrow('Parsing incomplete')
    }
  })
  it('accepts a completed result with less than one percent rejected rows', async () => {
    const result = { status: 'COMPLETED', source_count: 664076, parsed_count: 664075, stored_count: 664075, rejected_count: 1,
      files: [{ logfile_id: 'f1', status: 'COMPLETED', parsed_count: 664075, stored_count: 664075 }] }
    vi.mocked(apiRequest).mockResolvedValue(result)
    await expect(parseProjectFiles('p1', ['f1'])).resolves.toEqual(result)
    vi.mocked(apiRequest).mockResolvedValue({ ...result, source_count: 100, parsed_count: 99, stored_count: 99 })
    await expect(parseProjectFiles('p1', ['f1'])).rejects.toThrow('Parsing incomplete')
  })
  it('returns failure details for the blocking results dialog', async () => {
    const result = { status: 'FAILED', source_count: 100, parsed_count: 99, stored_count: 0, rejected_count: 1,
      files: [{ logfile_id: 'f1', status: 'FAILED', parsed_count: 99, stored_count: 0 }] }
    vi.mocked(apiRequest).mockResolvedValue(result)
    await expect(parseProjectFiles('p1', ['f1'])).resolves.toEqual(result)
  })
})
