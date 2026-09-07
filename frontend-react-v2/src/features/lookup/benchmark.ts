import type { LogRow } from './service'

export function createBenchmarkRows(count: number): LogRow[] {
  return Array.from({ length: count }, (_, index) => ({
    id: index + 1,
    line_no: index + 1,
    raw_log: `fixture request ${index + 1}`,
    project_id: 'fixture',
    logfile_id: 'fixture-log',
  }))
}
