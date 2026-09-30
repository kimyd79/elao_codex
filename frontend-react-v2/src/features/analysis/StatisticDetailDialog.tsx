import { useCallback, useEffect, useMemo, useState } from 'react'
import { createPortal } from 'react-dom'
import ReactECharts from 'echarts-for-react'
import { AgGridReact } from 'ag-grid-react'
import { AllCommunityModule, ModuleRegistry, type ColDef } from 'ag-grid-community'
import { fetchLogs, type LogRow } from '@/features/lookup/service'
import { combineRequestTime } from './requestTimeChart'
import { fetchChartData, type AnalysisQuery, type ChartPayload } from './service'
import { formatAxisTimestamp, timedSeries, timelineStepMs } from './timelineChart'

ModuleRegistry.registerModules([AllCommunityModule])

export type StatisticSelection = {
  type: number
  title: string
  value: string
}

const conditionByStatistic: Record<number, { code: string; label: string }> = {
  1: { code: 'S', label: 'Status' },
  2: { code: 'R', label: 'Request' },
  3: { code: 'NFR', label: 'Request (404)' },
  4: { code: 'R', label: 'Request' },
  5: { code: 'I', label: 'IP' },
  6: { code: 'E', label: 'Referrer' },
  7: { code: 'U', label: 'UserAgent' },
  8: { code: 'R', label: 'Request' },
  9: { code: 'F', label: 'Static file type' },
  10: { code: 'R', label: 'Request' },
  11: { code: 'R', label: 'Request' },
  12: { code: 'R', label: 'Request' },
  13: { code: 'V1', label: 'Upstream' },
  14: { code: 'V2', label: 'Domain' },
}

export function statisticCondition(type: number) {
  return conditionByStatistic[type]
}

function formatDate(value: unknown) {
  const text = String(value ?? '').replace(/[^0-9]/g, '')
  return text.length === 8 ? `${text.slice(0, 4)}/${text.slice(4, 6)}/${text.slice(6, 8)}` : String(value ?? '-')
}

function formatTime(value: unknown) {
  const text = String(value ?? '').replace(/[^0-9]/g, '').padStart(6, '0')
  return text.length === 6 ? `${text.slice(0, 2)}:${text.slice(2, 4)}:${text.slice(4, 6)}` : String(value ?? '-')
}

function formatNumber(value: unknown) {
  const number = Number(value)
  return Number.isFinite(number) ? number.toLocaleString() : '-'
}

function requestTimeOption(data: ChartPayload | null) {
  const labels = data?.resultX ?? []
  return {
    title: { text: 'Request (count) / Timetaken', left: 'center', top: 8, textStyle: { color: '#46329b', fontSize: 16 } },
    legend: { top: 36 },
    tooltip: { trigger: 'axis' },
    toolbox: {
      right: 12,
      top: 4,
      feature: {
        dataZoom: { yAxisIndex: 'none', title: { zoom: 'Drag to zoom', back: 'Reset zoom' } },
        restore: { title: 'Reset' },
      },
    },
    grid: { left: 58, right: 72, top: 88, bottom: 58, containLabel: true },
    xAxis: {
      type: 'time',
      minInterval: timelineStepMs(labels),
      axisLabel: { formatter: (value: number) => formatAxisTimestamp(value), hideOverlap: true },
    },
    yAxis: [
      { type: 'value', name: 'TPS', min: 0, nameTextStyle: { color: '#4056b5' }, axisLabel: { color: '#4056b5' } },
      { type: 'value', name: 'Timetaken (s)', min: 0, position: 'right', nameTextStyle: { color: '#df8626' }, axisLabel: { color: '#df8626' }, splitLine: { show: false } },
    ],
    dataZoom: [{ type: 'inside', zoomOnMouseWheel: true, moveOnMouseMove: true }],
    series: [
      { type: 'line', smooth: true, showSymbol: false, name: 'TPS', yAxisIndex: 0, itemStyle: { color: '#4056b5' }, data: timedSeries(labels, data?.resultY ?? []) },
      { type: 'line', smooth: true, showSymbol: false, name: 'Timetaken (s)', yAxisIndex: 1, itemStyle: { color: '#df8626' }, data: timedSeries(labels, data?.resultY_time ?? []), connectNulls: false },
    ],
  }
}

export function StatisticDetailDialog({ selection, query, onClose }: { selection: StatisticSelection; query: AnalysisQuery; onClose: () => void }) {
  const condition = statisticCondition(selection.type)
  const [rows, setRows] = useState<LogRow[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [tableLoading, setTableLoading] = useState(true)
  const [chartLoading, setChartLoading] = useState(true)
  const [tableError, setTableError] = useState('')
  const [chartError, setChartError] = useState('')
  const [chartData, setChartData] = useState<ChartPayload | null>(null)
  const [timeline, setTimeline] = useState('2')
  const pageSize = 20
  const totalPages = Math.max(1, Math.ceil(total / pageSize))
  const pageItems = Array.from(new Set([1, page - 2, page - 1, page, page + 1, page + 2, totalPages].filter((value) => value >= 1 && value <= totalPages)))
  const pageInputWidth = Math.max(64, String(totalPages).length * 8 + 42)

  const columns = useMemo<ColDef<LogRow>[]>(() => [
    { field: 'fdate', headerName: 'Date', width: 120, valueFormatter: (params) => formatDate(params.value) },
    { field: 'ftime', headerName: 'Time', width: 110, valueFormatter: (params) => formatTime(params.value) },
    { field: 'fip', headerName: 'IP', width: 150 },
    { field: 'frequest', headerName: 'Request', flex: 1, minWidth: 280 },
    { field: 'freferer', headerName: 'Referrer', flex: 1, minWidth: 180 },
    { field: 'fuser_agent', headerName: 'UserAgent', flex: 1, minWidth: 180 },
    { field: 'fstatus', headerName: 'Status', width: 90 },
    { field: 'fbyte', headerName: 'Byte', width: 110, type: 'numericColumn', cellStyle: { textAlign: 'right' }, valueFormatter: (params) => formatNumber(params.value) },
    { field: 'ftime_taken', headerName: 'TimeTaken (μs)', width: 145, type: 'numericColumn', cellStyle: { textAlign: 'right' }, valueFormatter: (params) => formatNumber(params.value) },
  ], [])

  const loadTable = useCallback(async (targetPage: number, signal?: AbortSignal) => {
    if (!condition || !query.project_id) return
    setTableLoading(true)
    setTableError('')
    try {
      const result = await fetchLogs({
        projectId: String(query.project_id),
        limit: pageSize,
        offset: (targetPage - 1) * pageSize,
        condition: String(query.conditionValue ?? ''),
        search: String(query.searchValue ?? ''),
        excludeSearch: String(query.excludeSearch) === 'true',
        dateFrom: query.dateFromValue ? String(query.dateFromValue) : undefined,
        dateTo: query.dateToValue ? String(query.dateToValue) : undefined,
        timeFrom: query.timeFromValue ? String(query.timeFromValue) : undefined,
        timeTo: query.timeToValue ? String(query.timeToValue) : undefined,
        ttFrom: query.ttFromValue ? String(query.ttFromValue) : undefined,
        ttTo: query.ttToValue ? String(query.ttToValue) : undefined,
        server: Array.isArray(query.projectServers) ? query.projectServers.join(',') : String(query.projectServers ?? ''),
        detailCondition: condition.code,
        detailSearch: selection.value,
      }, signal)
      if (signal?.aborted) return
      setRows(result.results ?? result.items ?? [])
      setTotal(result.count ?? (result.results ?? result.items ?? []).length)
      setPage(targetPage)
    } catch (reason) {
      if (signal?.aborted) return
      setTableError(reason instanceof Error ? reason.message : '상세 로그를 조회하지 못했습니다.')
    } finally {
      if (!signal?.aborted) setTableLoading(false)
    }
  }, [condition, query, selection.value])

  useEffect(() => {
    const controller = new AbortController()
    void loadTable(1, controller.signal)
    return () => controller.abort()
  }, [loadTable])

  useEffect(() => {
    if (!condition || !query.project_id) return
    const controller = new AbortController()
    const filteredQuery: AnalysisQuery = {
      ...query,
      type: timeline,
      detailconditionValue: condition.code,
      detailsearchValue: selection.value,
    }
    setChartLoading(true)
    setChartError('')
    void Promise.all([
      fetchChartData({ ...filteredQuery, kind: 1 }, controller.signal),
      fetchChartData({ ...filteredQuery, kind: 3 }, controller.signal),
    ]).then(([requests, time]) => {
      if (!controller.signal.aborted) setChartData(combineRequestTime(requests, time))
    }).catch((reason: unknown) => {
      if (!controller.signal.aborted) setChartError(reason instanceof Error ? reason.message : '차트를 조회하지 못했습니다.')
    }).finally(() => {
      if (!controller.signal.aborted) setChartLoading(false)
    })
    return () => controller.abort()
  }, [condition, query, selection.value, timeline])

  useEffect(() => {
    const closeOnEscape = (event: KeyboardEvent) => { if (event.key === 'Escape') onClose() }
    window.addEventListener('keydown', closeOnEscape)
    return () => window.removeEventListener('keydown', closeOnEscape)
  }, [onClose])

  if (!condition) return null
  return createPortal(
    <div className="statistic-detail-backdrop" role="presentation" onMouseDown={onClose}>
      <section className="statistic-detail-dialog" role="dialog" aria-modal="true" aria-labelledby="statistic-detail-title" onMouseDown={(event) => event.stopPropagation()}>
        <header className="statistic-detail-header">
          <div>
            <p className="auth-kicker">STATISTICS DETAIL</p>
            <h2 id="statistic-detail-title">{condition.label} condition: {selection.value}</h2>
            <p>{selection.title} · 현재 Search 조건에 <strong>{condition.label}</strong> = <strong>{selection.value}</strong> 조건을 추가한 결과입니다.</p>
          </div>
          <button type="button" className="detail-close-button" onClick={onClose}>Close</button>
        </header>

        <section className="statistic-detail-section" aria-busy={tableLoading}>
          <div className="statistic-detail-section-heading"><h3>Log details</h3><span>Total {total.toLocaleString()}</span></div>
          {tableError && <p role="alert" className="statistic-detail-error">{tableError}</p>}
          <div className="ag-theme-quartz statistic-detail-grid"><AgGridReact rowData={rows} columnDefs={columns} loading={tableLoading} domLayout="autoHeight" /></div>
          <div className="detail-pagination detail-pagination-image statistic-detail-pagination">
            <button type="button" className="page-arrow" disabled={tableLoading || page <= 1} onClick={() => void loadTable(page - 1)} aria-label="Previous page">‹</button>
            {pageItems.map((item, index) => <span key={item}>{index > 0 && item > pageItems[index - 1] + 1 && <span className="page-ellipsis">...</span>}<button type="button" className={item === page ? 'page-number active' : 'page-number'} disabled={tableLoading || item === page} onClick={() => void loadTable(item)}>{item}</button></span>)}
            <button type="button" className="page-arrow" disabled={tableLoading || page >= totalPages} onClick={() => void loadTable(page + 1)} aria-label="Next page">›</button>
            <label className="page-go"><input type="number" min={1} max={totalPages} defaultValue={page} key={page} style={{ width: pageInputWidth }} aria-label={`Page number, maximum ${totalPages}`} onKeyDown={(event) => { if (event.key === 'Enter') { const value = Math.min(totalPages, Math.max(1, Number(event.currentTarget.value))); void loadTable(value) } }} /><button type="button" onClick={(event) => { const input = event.currentTarget.previousElementSibling as HTMLInputElement; const value = Math.min(totalPages, Math.max(1, Number(input.value))); void loadTable(value) }}>GO</button></label>
          </div>
        </section>

        <section className="statistic-detail-section statistic-detail-chart-section" aria-busy={chartLoading}>
          <div className="statistic-detail-chart-toolbar">
            <strong>Timeline</strong>
            {[['1', 'HH'], ['2', 'HHMM'], ['3', 'HHMMSS']].map(([value, label]) => (
              <label className="inline-check" key={value}><input type="radio" name="statistic-detail-timeline" checked={timeline === value} onChange={() => setTimeline(value)} />{label}</label>
            ))}
            <span>차트 우측 상단의 확대 도구를 선택한 후 그래프를 드래그하세요.</span>
          </div>
          {chartError && <p role="alert" className="statistic-detail-error">{chartError}</p>}
          <ReactECharts option={requestTimeOption(chartData)} style={{ width: '100%', height: 390 }} autoResize notMerge lazyUpdate />
          {chartLoading && <div className="query-overlay"><span className="query-loading" role="status"><span className="query-spinner" aria-hidden="true" />데이터 조회 중…</span></div>}
        </section>
      </section>
    </div>,
    document.body,
  )
}
