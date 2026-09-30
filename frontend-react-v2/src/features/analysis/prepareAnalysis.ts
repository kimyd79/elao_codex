import { apiRequest } from '@/lib/api/client'
import { listLogFiles, listProjects, type LogFileSummary, type ProjectSummary } from '@/features/init/service'
import { fetchChartData, fetchPeriod, fetchStatistics, type AnalysisQuery, type ChartPayload } from './service'
import { combineRequestTime } from './requestTimeChart'

export type PreparedAnalysis = {
  projectId: string
  project?: ProjectSummary
  files: LogFileSummary[]
  total: number
  period: Awaited<ReturnType<typeof fetchPeriod>>
  query: AnalysisQuery
  charts: Partial<Record<'tps' | 'request' | 'statusPie' | 'statusBar' | 'visitor' | 'static', ChartPayload>>
  statistics: Record<number, Array<{ result?: unknown; result_count?: unknown; result_per?: unknown }>>
}
let prepared: PreparedAnalysis | undefined
export function takePreparedAnalysis(projectId: string) {
  return prepared?.projectId === projectId ? prepared : undefined
}

export async function prepareAnalysis(projectId: string, onProgress: (text: string) => void) {
  prepared = undefined
  onProgress('프로젝트 정보와 분석 기간을 불러오는 중…')
  const [projects, files, period, total] = await Promise.all([
    listProjects(), listLogFiles(projectId), fetchPeriod(projectId),
    apiRequest<{ results?: Array<{ result_count?: number }> }>({
      method: 'POST', url: '/logdetail_dynamic/statistics/', data: { project_id: projectId, type: 0, N: 0 },
    }),
  ])
  const query: AnalysisQuery = {
    project_id: projectId, conditionValue: 'N', searchValue: '', excludeSearch: 'false',
    projectServers: [...new Set((files.results ?? []).map((file) => `${file.server_name ?? '-'}-${file.instance_name ?? '-'}`))],
    dateFromValue: period.start_date ?? '', dateToValue: period.end_date ?? '',
    timeFromValue: period.start_time ?? '', timeToValue: period.end_time ?? '',
    ttFromValue: '', ttToValue: '',
  }
  const totalCount = Number(total.results?.[0]?.result_count ?? 0)
  const chartResults: Record<number, ChartPayload> = {}
  const statisticResults: Record<number, ChartPayload> = {}
  const tasks = [
    ...[1, 2, 3].map((kind) => async () => { chartResults[kind] = await fetchChartData({ ...query, type: '1', kind }) }),
    ...Array.from({ length: 14 }, (_, i) => i + 1).map((type) => async () => {
      const result = await fetchStatistics({ ...query, type, N: 5, include_total: false })
      if (!Array.isArray(result.results)) throw new Error('통계 응답을 확인할 수 없습니다.')
      statisticResults[type] = result
    }),
  ]
  let completed = 0
  // Limit concurrent database aggregations for large uploaded files.
  for (let i = 0; i < tasks.length; i += 3) {
    const results = await Promise.allSettled(tasks.slice(i, i + 3).map(async (task) => {
      await task()
      onProgress(`분석 데이터 로딩 중… ${++completed}/${tasks.length}`)
    }))
    const failure = results.find((result) => result.status === 'rejected')
    if (failure?.status === 'rejected') throw failure.reason
  }
  prepared = {
    projectId, project: projects.results?.find((p) => String(p.project_id) === projectId),
    files: files.results ?? [], period, query, total: totalCount,
    charts: { tps: chartResults[1], statusBar: chartResults[2], request: combineRequestTime(chartResults[1], chartResults[3]),
      statusPie: statisticResults[1], visitor: statisticResults[5], static: statisticResults[9] },
    statistics: Object.fromEntries(Object.entries(statisticResults).map(([key, result]) => [key,
      (result.results as PreparedAnalysis['statistics'][number]).map((row) => {
        const type = Number(key)
        const percentageTotal = type === 8 ? Number(result.totalCnt ?? 0) : totalCount
        return {
          ...row,
          result_per: [4, 10, 11].includes(type) ? undefined
            : percentageTotal > 0
              ? Number(row.result_count ?? 0) / percentageTotal * 100
              : 0,
        }
      }),
    ])),
  }
  return prepared
}

export function clearPreparedAnalysis() { prepared = undefined }
