import { apiRequest } from '@/lib/api/client'

export type AnalysisQuery = Record<string, string | number | string[] | undefined>

export function toAnalysisRequest(query: AnalysisQuery) {
  const { project_id, type = '1', kind = 1, ...filter } = query
  // DynamicLogDetailViewSet reads project_id both from the request body and
  // from filter when constructing the project-specific dynamic model.
  return { project_id, type, kind, filter: { ...filter, project_id } }
}

export type ChartPayload = {
  resultX?: string[]
  resultY?: number[]
  resultY_time?: number[]
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
    data: { ...toAnalysisRequest(query), N: 1 },
    signal,
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
