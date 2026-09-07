import { apiRequest } from '@/lib/api/client'

export type LogRow = Record<string, unknown> & {
  id?: string | number
  logfile_id?: string | number
  line_no?: number
  raw_log?: string
}
export type LogQuery = {
  projectId?: string
  cursor?: string | null
  limit?: number
  offset?: number
  search?: string
  excludeSearch?: boolean
  dateFrom?: string
  dateTo?: string
  server?: string
}
export type LogPage = {
  results?: LogRow[]
  items?: LogRow[]
  next_cursor?: string | null
  next?: string | null
  count?: number
}

export async function fetchLogs(query: LogQuery, signal?: AbortSignal) {
  const params = {
    project_id: query.projectId,
    cursor: query.cursor ?? undefined,
    limit: query.limit ?? 100,
    offset: query.offset ?? undefined,
    searchValue: query.search,
    excludeSearch: query.excludeSearch,
    dateFromValue: query.dateFrom,
    dateToValue: query.dateTo,
    projectServers: query.server,
  }
  return apiRequest<LogPage>({ method: 'GET', url: '/logdetail_dynamic/', params, signal })
}

export async function fetchLogContext(
  payload: {
    project_id: string
    logfile_id?: string | number
    line_no?: number
    before?: number
    after?: number
  },
  signal?: AbortSignal,
) {
  return apiRequest<{ before?: LogRow[]; after?: LogRow[]; item?: LogRow }>({
    method: 'POST',
    url: '/logdetail_dynamic/get_before_after_detail/',
    data: payload,
    signal,
  })
}
