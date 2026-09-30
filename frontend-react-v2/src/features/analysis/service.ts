import { apiRequest } from '@/lib/api/client'

export type AnalysisQuery = Record<string, string | number | boolean | string[] | undefined>

export function toAnalysisRequest(query: AnalysisQuery) {
  const { project_id, type = '1', kind = 1, ...filter } = query
  delete filter.N
  delete filter.include_total
  // DynamicLogDetailViewSet reads project_id both from the request body and
  // from filter when constructing the project-specific dynamic model.
  return {
    project_id,
    type,
    kind,
    filter: {
      dateFromValue: '',
      dateToValue: '',
      timeFromValue: '',
      timeToValue: '',
      ttFromValue: '',
      ttToValue: '',
      conditionValue: '',
      searchValue: '',
      ...filter,
      project_id,
      excludeSearch: String(filter.excludeSearch) === 'true',
      projectServers: Array.isArray(filter.projectServers)
        ? filter.projectServers
        : String(filter.projectServers ?? '')
            .split(',')
            .filter(Boolean),
    },
  }
}

export function toStatisticsRequest(query: AnalysisQuery) {
  return {
    ...toAnalysisRequest(query),
    type: Number(query.type ?? 1),
    N: Number(query.N ?? 5),
    include_total: query.include_total !== false,
  }
}

export type ChartPayload = {
  resultX?: string[]
  resultY?: number[]
  resultY_time?: Array<number | null>
  resultY_200?: number[]
  resultY_300?: number[]
  resultY_400?: number[]
  resultY_500?: number[]
  resultXY?: Array<{ name?: string; value?: number | string }>
  resultXY2?: Array<{ name?: string; value?: number | string }>
  result_time_unit?: string
  resultY_time_unit?: string
  [key: string]: unknown
}

export type XViewPayload = {
  limit_exceeded?: boolean
  message?: string
  uris: Array<{ uri: string; count: number }>
  points: Array<{
    time: string
    response_time_ms: number
    status_group: '20x' | '30x' | '40x' | '50x' | 'other'
  }>
  total_count: number
  displayed_count: number
  sampled: boolean
  sample_stride: number
}

export function fetchChartData(query: AnalysisQuery, signal?: AbortSignal) {
  return apiRequest<ChartPayload>({
    method: 'POST',
    url: '/logdetail_dynamic/chartdata/',
    data: toAnalysisRequest(query),
    signal,
  })
}

export function fetchStatistics(query: AnalysisQuery, signal?: AbortSignal) {
  return apiRequest<ChartPayload>({
    method: 'POST',
    url: '/logdetail_dynamic/statistics/',
    data: toStatisticsRequest(query),
    // Statistics aggregate a potentially large project table. The default
    // 30-second API timeout is appropriate for interactive endpoints but can
    // expire while the server is still legitimately completing this query.
    timeout: 120_000,
    signal,
  })
}

export function fetchXView(query: AnalysisQuery, signal?: AbortSignal) {
  return apiRequest<XViewPayload>({
    method: 'POST',
    url: '/logdetail_dynamic/xview/',
    data: { ...toAnalysisRequest(query), uri_limit: 20 },
    timeout: 120_000,
    signal,
  })
}

export type XViewBounds = { start: string; end: string; lower: number; upper: number }
export function fetchXViewDetails(query: AnalysisQuery, bounds: XViewBounds, page: number, signal?: AbortSignal, ordering = 'fdatetime') {
  return apiRequest<{ count: number; results: Array<Record<string, string | number>> }>({
    method: 'POST', url: '/logdetail_dynamic/xview_details/',
    data: { ...toAnalysisRequest(query), bounds, ordering, limit: 20, offset: (page - 1) * 20 }, signal,
  })
}

export function fetchComparison(query: AnalysisQuery, signal?: AbortSignal) {
  return apiRequest<ChartPayload>({
    method: 'POST',
    url: '/logdetail_dynamic/chartdata_diff/',
    data: toAnalysisRequest(query),
    signal,
  })
}
export function fetchPeriod(projectId: string, creator = 'admin') {
  return apiRequest<{
    start_date?: string
    start_time?: string
    end_date?: string
    end_time?: string
  }>({
    method: 'POST',
    url: '/logdetail_dynamic/start_end/',
    data: { project_id: projectId, creator },
  })
}
