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
  condition?: string
  search?: string
  excludeSearch?: boolean
  dateFrom?: string
  dateTo?: string
  timeFrom?: string
  timeTo?: string
  ttFrom?: string
  ttTo?: string
  server?: string
  detailCondition?: string
  detailSearch?: string
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
    // Empty icontains values are interpreted as no matches by the legacy
    // dynamic endpoint, so omit inactive filters entirely.
    conditionValue: query.condition && query.condition !== 'N' ? query.condition : undefined,
    searchValue: query.search || undefined,
    excludeSearch: query.excludeSearch ? true : undefined,
    dateFromValue: query.dateFrom,
    dateToValue: query.dateTo,
    timeFromValue: query.timeFrom,
    timeToValue: query.timeTo,
    ttFromValue: query.ttFrom,
    ttToValue: query.ttTo,
    projectServers: query.server,
    detailconditionValue: query.detailCondition,
    detailsearchValue: query.detailSearch,
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
