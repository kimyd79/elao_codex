import { useEffect, useMemo, useRef, useState } from 'react'
import ReactECharts from 'echarts-for-react'
import { useSearchParams } from 'react-router-dom'
import { listLogFiles } from '@/features/init/service'
import { ApiError } from '@/lib/api/errors'
import { fetchChartData, fetchStatistics, type AnalysisQuery, type ChartPayload } from './service'
import { combineRequestTime } from './requestTimeChart'
import { StatisticDetailDialog, type StatisticSelection } from './StatisticDetailDialog'
import { formatAxisTimestamp, showTimelineSymbols, timedSeries, timelineStepMs } from './timelineChart'
import type { PreparedAnalysis } from './prepareAnalysis'

type ChartId = 'tps' | 'request' | 'statusPie' | 'statusBar' | 'visitor' | 'static'
const charts: Array<{ id: ChartId; label: string; buttonLabel: string }> = [
  { id: 'tps', label: 'Transaction Per Second', buttonLabel: 'TPS' },
  { id: 'request', label: 'Request (count) / Timetaken', buttonLabel: 'Req/Timetaken' },
  { id: 'statusPie', label: 'HTTP Status Codes', buttonLabel: 'Http Status(P)' },
  { id: 'statusBar', label: 'Http Status Codes', buttonLabel: 'Http Status(T)' },
  { id: 'visitor', label: 'Visitor IP top5', buttonLabel: 'Visitor IP(5)' },
  { id: 'static', label: 'Static File types', buttonLabel: 'Static File' },
]

function formatTimeline(value: unknown) {
  const raw = String(value ?? '')
  const digits = raw.replace(/\D/g, '')
  if (digits.length < 8) return raw
  const date = `${digits.slice(0, 4)}-${digits.slice(4, 6)}-${digits.slice(6, 8)}`
  if (digits.length < 10) return date
  if (digits.length < 12) return `${date} ${digits.slice(8, 10)}:00:00`
  if (digits.length < 14) return `${date} ${digits.slice(8, 10)}:${digits.slice(10, 12)}:00`
  return `${date} ${digits.slice(8, 10)}:${digits.slice(10, 12)}:${digits.slice(12, 14)}`
}

function lineOption(data: ChartPayload | null, title: string, time = false) {
  const labels = data?.resultX ?? []
  const tpsSeries = timedSeries(labels, data?.resultY ?? [])
  const responseTimeSeries = timedSeries(labels, data?.resultY_time ?? [])
  const showSymbols = showTimelineSymbols(labels)
  return {
    title: { text: title, left: 'center', top: 6, textStyle: { color: '#46329b', fontSize: 16 } },
    legend: { top: 32 },
    tooltip: { trigger: 'axis' },
    toolbox: {
      right: 12,
      top: 2,
      feature: {
        dataZoom: {
          yAxisIndex: 'none',
          title: { zoom: 'Drag to zoom', back: 'Reset zoom' },
        },
      },
    },
    grid: { left: 58, right: time ? 72 : 24, top: time ? 88 : 72, bottom: 72, containLabel: true },
    xAxis: {
      type: 'time',
      minInterval: timelineStepMs(labels),
      axisLabel: { formatter: (value: number) => formatAxisTimestamp(value), hideOverlap: true },
    },
    yAxis: time ? [
      { type: 'value', name: 'TPS', position: 'left', min: 0, nameTextStyle: { color: '#4056b5' }, axisLabel: { color: '#4056b5' } },
      { type: 'value', name: 'Timetaken (s)', position: 'right', min: 0, nameTextStyle: { color: '#df8626' }, axisLabel: { color: '#df8626' }, splitLine: { show: false } },
    ] : { type: 'value' },
    // Zoom is selected by dragging directly across the plot. Keep inside
    // wheel/pinch zoom for trackpads while avoiding a separate bottom slider.
    dataZoom: [{ type: 'inside', zoomOnMouseWheel: true, moveOnMouseMove: true }],
    series: [
      {
        type: 'line',
        smooth: true,
        showSymbol: showSymbols,
        symbolSize: 5,
        name: 'TPS',
        yAxisIndex: 0,
        itemStyle: { color: '#4056b5' },
        data: tpsSeries,
      },
      ...(time ? [{
        type: 'line', smooth: true, showSymbol: showSymbols, symbolSize: 5,
        name: 'Timetaken (s)', yAxisIndex: 1,
        itemStyle: { color: '#df8626' },
        data: responseTimeSeries,
        connectNulls: false,
      }] : []),
    ],
  }
}
function statusBarOption(data: ChartPayload | null) {
  const x = (data?.resultX ?? []).map(formatTimeline)
  return {
    animation: false,
    title: {
      text: 'Http Status Codes',
      left: 'center',
      top: 6,
      textStyle: { color: '#46329b', fontSize: 16 },
    },
    tooltip: { trigger: 'axis' },
    legend: { top: 32 },
    toolbox: {
      right: 12,
      top: 2,
      feature: {
        dataZoom: {
          yAxisIndex: 'none',
          title: { zoom: 'Drag to zoom', back: 'Reset zoom' },
        },
      },
    },
    grid: { left: 48, right: 18, top: 72, bottom: 72 },
    xAxis: { type: 'category', data: x },
    yAxis: { type: 'value' },
    dataZoom: [{ type: 'inside', zoomOnMouseWheel: true, moveOnMouseMove: true }],
    series: [
      { name: '200', type: 'bar', large: true, progressive: 5000, data: data?.resultY_200 ?? [] },
      { name: '300', type: 'bar', large: true, progressive: 5000, data: data?.resultY_300 ?? [] },
      { name: '400', type: 'bar', large: true, progressive: 5000, data: data?.resultY_400 ?? [] },
      { name: '500', type: 'bar', large: true, progressive: 5000, data: data?.resultY_500 ?? [] },
    ],
  }
}
function pieOption(data: ChartPayload | null, title: string) {
  const rows = (data?.results ?? data?.resultXY ?? []) as Array<Record<string, unknown>>
  const values = rows.map((r) => ({
    name: String(r.result ?? r.name ?? r.x ?? '-'),
    value: Number(r.result_count ?? r.value ?? r.y ?? 0),
  }))
  return {
    title: { text: title, left: 'center', top: 6, textStyle: { color: '#46329b', fontSize: 16 } },
    tooltip: { trigger: 'item' },
    legend: { top: 34, type: 'scroll' },
    series: [
      {
        type: 'pie',
        top: 64,
        radius: ['35%', '68%'],
        data: values,
        label: { formatter: '{b}' },
      },
    ],
  }
}

export function AnalysisChartPage({ eventName = 'elao:analysis-search', initial: prepared }: { eventName?: string; initial?: PreparedAnalysis }) {
  const initial = useMemo(
    () => Object.fromEntries(new URLSearchParams(window.location.search)),
    [],
  ) as AnalysisQuery
  const [timeline, setTimeline] = useState(String(initial.type ?? '1'))
  const [query, setQuery] = useState<AnalysisQuery>(prepared?.query ?? initial)
  const [data, setData] = useState<Partial<Record<ChartId, ChartPayload>>>(prepared?.charts ?? {})
  const [chartStates, setChartStates] = useState<Partial<Record<ChartId, string>>>(
    prepared ? Object.fromEntries(charts.map(({ id }) => [id, 'complete'])) : {},
  )
  const requestControllers = useRef<Partial<Record<ChartId, AbortController>>>({})
  const loadingCount = Object.values(chartStates).filter((state) => state === 'loading').length

  const load = async (id: ChartId, sourceQuery = query, sourceTimeline = timeline) => {
    requestControllers.current[id]?.abort()
    const controller = new AbortController()
    requestControllers.current[id] = controller
    const params = {
      ...sourceQuery,
      type: sourceTimeline,
      kind: id === 'tps' ? 1 : id === 'request' ? 3 : 2,
    }
    setChartStates((current) => ({ ...current, [id]: 'loading' }))
    try {
      const result =
        id === 'statusPie' || id === 'visitor' || id === 'static'
          ? await fetchStatistics({
              ...params,
              type: id === 'statusPie' ? 1 : id === 'visitor' ? 5 : 9,
            }, controller.signal)
          : id === 'request'
            ? await Promise.all([
                fetchChartData({ ...params, kind: 1 }, controller.signal),
                fetchChartData(params, controller.signal),
              ]).then(([tps, time]) => combineRequestTime(tps, time))
            : await fetchChartData(params, controller.signal)
      if (controller.signal.aborted) return
      setData((current) => ({ ...current, [id]: result }))
      setChartStates((current) => ({ ...current, [id]: 'complete' }))
    } catch {
      if (controller.signal.aborted) return
      setChartStates((current) => ({ ...current, [id]: 'error' }))
    }
  }
  const loadAll = async (sourceQuery = query, sourceTimeline = timeline) => {
    await Promise.allSettled(charts.map((chart) => load(chart.id, sourceQuery, sourceTimeline)))
  }
  useEffect(() => {
    const controllers = requestControllers.current
    const handler = (event: Event) => {
      const detail = (event as CustomEvent<AnalysisQuery>).detail
      const nextTimeline = String(detail.type ?? '1')
      setQuery(detail)
      setTimeline(nextTimeline)
      void loadAll(detail, nextTimeline)
    }
    window.addEventListener(eventName, handler)
    return () => {
      window.removeEventListener(eventName, handler)
      Object.values(controllers).forEach((controller) => controller.abort())
    }
    // The loader intentionally uses the latest event payload and is not a hook dependency.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
  const refreshAll = () => {
    void loadAll()
  }
  return (
    <div className="chart-workspace">
      <div className="chart-filters">
        <div className="chart-filter-row">
          <strong>Timeline</strong>
          {[
            ['1', 'HH'],
            ['2', 'HHMM'],
            ['3', 'HHMMSS'],
          ].map(([value, label]) => (
            <label className="inline-check" key={value}>
              <input
                type="radio"
                name={`${eventName}-timeline`}
                checked={timeline === value}
                onChange={() => setTimeline(value)}
              />
              {label}
            </label>
          ))}
        </div>
        <div className="chart-filter-row">
          <strong>Charts</strong>
          {charts.map((chart) => (
            <button
              type="button"
              key={chart.id}
              className="chart-selector"
              disabled={chartStates[chart.id] === 'loading'}
              onClick={() => void load(chart.id)}
            >
              {chartStates[chart.id] === 'loading' ? `${chart.buttonLabel} · 조회 중` : chart.buttonLabel}
            </button>
          ))}
          <button type="button" onClick={refreshAll} disabled={loadingCount > 0}>
            ALL
          </button>
        </div>
      </div>
      <p role="status" className="query-progress">
        {loadingCount > 0 ? `차트 조회 중 · ${loadingCount}개 남음` : Object.values(chartStates).includes('error') ? '일부 차트 조회 실패 · 해당 차트 버튼으로 다시 조회하세요.' : Object.keys(chartStates).length ? '차트 조회 완료' : '조회할 차트를 선택하세요.'}
      </p>
      <div className="chart-grid">
        {charts.map((chart) => {
          const chartData = data[chart.id] ?? null
          const option =
            chart.id === 'tps'
              ? lineOption(chartData, chart.label)
              : chart.id === 'request'
                ? lineOption(chartData, chart.label, true)
                : chart.id === 'statusBar'
                  ? statusBarOption(chartData)
                  : pieOption(chartData, chart.label)
          return (
            <div className="chart-card query-region" key={chart.id} aria-label={chart.label} aria-busy={chartStates[chart.id] === 'loading'}>
              <div className="analysis-chart-canvas">
                <ReactECharts option={option} style={{ height: '100%', width: '100%' }} autoResize notMerge lazyUpdate />
              </div>
              {chartStates[chart.id] === 'loading' && <div className="query-overlay"><LoadingIndicator /></div>}
              {chartStates[chart.id] === 'error' && <div className="query-overlay" role="alert">조회하지 못했습니다. 다시 조회해 주세요.</div>}
            </div>
          )
        })}
      </div>
    </div>
  )
}

const statisticCards = [
  [2, 'Requests URI (count)'],
  [5, 'Visitors (count)'],
  [4, 'Requests Time-taken (s/㎲)'],
  [11, 'Requests Average Time-taken (s/㎲)'],
  [1, 'HTTP Status Codes (count)'],
  [3, '404 Requests URI (count)'],
  [8, 'Requests URI (Total MB)'],
  [10, 'Requests URI (Average MB)'],
  [6, 'Referers (count)'],
  [7, 'User Agent (count)'],
  [12, 'Static file Names (count)'],
  [9, 'Static files (count)'],
  [13, 'Upstream Info (count)'],
  [14, 'Domains (count, K8S Ingress)'],
] as const

const STATISTICS_CONCURRENCY = 3

async function forEachWithConcurrency<T>(
  items: readonly T[],
  concurrency: number,
  callback: (item: T) => Promise<void>,
) {
  let nextIndex = 0
  const worker = async () => {
    while (nextIndex < items.length) {
      const item = items[nextIndex++]
      await callback(item)
    }
  }
  await Promise.all(
    Array.from({ length: Math.min(concurrency, items.length) }, () => worker()),
  )
}

type StatisticRow = { result?: unknown; result_count?: unknown; result_per?: unknown }

const BYTE_STATISTIC_TYPES = new Set([8, 10])
const BYTES_PER_MB = 1024 * 1024

function formatStatisticResult(type: number, value: unknown) {
  const numericValue = Number(value ?? 0)
  if (!BYTE_STATISTIC_TYPES.has(type)) return numericValue.toLocaleString()
  return `${(numericValue / BYTES_PER_MB).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })} MB`
}

function LoadingIndicator() {
  return <span className="query-loading" role="status"><span className="query-spinner" aria-hidden="true" />데이터 조회 중…</span>
}

function StatisticTable({
  type,
  title,
  rows,
  n,
  message,
  onSelect,
}: {
  type: number
  title: string
  rows: StatisticRow[]
  n: number
  message?: string
  onSelect: (selection: StatisticSelection) => void
}) {
  return (
    <div className="statistic-table-wrap" aria-busy={message?.startsWith('Loading')}>
      <h3 className="statistic-table-title">{title}</h3>
      <table className="statistic-table">
        <thead>
          <tr>
            <th>Top {n}</th>
            <th>{title}</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {message || !rows.length ? (
            <tr>
              <td colSpan={3}>{message?.startsWith('Loading') ? <LoadingIndicator /> : message || 'No matching data.'}</td>
            </tr>
          ) : (
            rows.map((row, index) => (
              <tr
                key={index}
                className="statistic-clickable-row"
                tabIndex={0}
                onClick={() => onSelect({ type, title, value: String(row.result ?? '') })}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault()
                    onSelect({ type, title, value: String(row.result ?? '') })
                  }
                }}
              >
                <td>{index + 1}</td>
                <td>{String(row.result ?? '-')}</td>
                <td>
                  {formatStatisticResult(type, row.result_count)}
                  {row.result_per !== undefined && (
                    <small> ({Number(row.result_per).toFixed(2)}%)</small>
                  )}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

export function StatisticsPage({ eventName = 'elao:analysis-search', manual = false, initial: prepared }: { eventName?: string; manual?: boolean; initial?: PreparedAnalysis }) {
  const [n, setN] = useState(5)
  const [params] = useSearchParams()
  const projectId = params.get('project_id') ?? ''
  const [query, setQuery] = useState<AnalysisQuery>(prepared?.query ?? {})
  const [rows, setRows] = useState<Record<number, StatisticRow[]>>(prepared?.statistics ?? {})
  const [messages, setMessages] = useState<Record<number, string>>({})
  const [status, setStatus] = useState(prepared ? '' : 'Loading project instances...')
  const [revision, setRevision] = useState(0)
  const [selection, setSelection] = useState<StatisticSelection | null>(null)
  const loadingCount = Object.values(messages).filter((message) => message === 'Loading...').length
  const progressText = loadingCount > 0
    ? `통계 조회 중 · ${statisticCards.length - loadingCount}/${statisticCards.length}개 처리 완료`
    : Object.values(messages).some(Boolean)
      ? '일부 통계 조회 실패 · 아래 표의 안내를 확인하세요.'
      : '통계 조회 완료'
  useEffect(() => {
    let active = true
    let searched = false
    const handler = (event: Event) => {
      searched = true
      setSelection(null)
      setQuery((event as CustomEvent<AnalysisQuery>).detail)
    }
    window.addEventListener(eventName, handler)
    const initial = Object.fromEntries(new URLSearchParams(window.location.search))
    if (manual) {
      setStatus('Set conditions and click Search.')
    } else if (projectId && !prepared) {
      void listLogFiles(projectId)
        .then((result) => {
          if (!active || searched) return
          const instances = [
            ...new Set(
              (result.results ?? []).map(
                (file) => `${file.server_name ?? '-'}-${file.instance_name ?? '-'}`,
              ),
            ),
          ]
          setQuery({
            ...initial,
            project_id: projectId,
            projectServers:
              initial.projectServers === undefined ? instances : initial.projectServers,
          })
        })
        .catch(() => {
          if (active && !searched)
            setStatus('Could not load project instances. Run Search to retry.')
        })
    } else if (!projectId) setStatus('Select a project to load statistics.')
    return () => {
      active = false
      window.removeEventListener(eventName, handler)
    }
  }, [projectId, eventName, manual, prepared])
  useEffect(() => {
    if (!query.project_id || query.project_id !== projectId) return
    if (prepared && query === prepared.query && n === 5 && revision === 0) return
    const controller = new AbortController()
    setStatus('')
    setRows({})
    setMessages(Object.fromEntries(statisticCards.map(([type]) => [type, 'Loading...'])))
    const loadType = async (type: number, sharedTotal?: number, includeTotal = true) => {
      if (controller.signal.aborted) return
      try {
        const result = await fetchStatistics(
          { ...query, type, N: n, include_total: includeTotal },
          controller.signal,
        )
        if (controller.signal.aborted) return
        if (!Array.isArray(result.results)) throw new Error('Invalid statistics response')
        // Total-byte percentages must use the API's byte-sum denominator.
        // The shared total is a request count and would make these percentages
        // many orders of magnitude too large.
        const total = type === 8
          ? Number(result.totalCnt ?? 0)
          : sharedTotal ?? Number(result.totalCnt ?? 0)
        const values = (result.results as StatisticRow[]).map((row) => ({
          ...row,
          result_per: [4, 10, 11].includes(type)
            ? undefined
            : total > 0
              ? (Number(row.result_count ?? 0) / total) * 100
              : 0,
        }))
        setRows((current) => ({ ...current, [type]: values }))
        setMessages((current) => ({ ...current, [type]: '' }))
        return Number(result.totalCnt ?? 0)
      } catch (error: unknown) {
        if (controller.signal.aborted) return
        const reason =
          error instanceof ApiError
            ? error.status
              ? `HTTP ${error.status}`
              : /timeout/i.test(error.message)
                ? 'Request timed out'
                : 'Network error'
            : 'Invalid response'
        setMessages((current) => ({
          ...current,
          [type]: `Unable to load (${reason}). Retry or run Search.`,
        }))
      }
      return undefined
    }
    void (async () => {
      // Load one low-cardinality aggregation with the total count first, then
      // reuse that denominator for every other percentage table. This removes
      // nine redundant COUNT(*) scans per statistics refresh.
      const total = await loadType(1)
      if (controller.signal.aborted) return
      const remaining = statisticCards.filter(([type]) => type !== 1)
      await forEachWithConcurrency(remaining, STATISTICS_CONCURRENCY, async ([type]) => {
        await loadType(type, total, total === undefined)
      })
    })()
    return () => controller.abort()
  }, [query, n, projectId, revision, prepared])
  return (
    <div className="statistics-workspace">
      <div className="statistics-controls">
        <strong>Select N</strong>
        <select value={n} onChange={(event) => setN(Number(event.target.value))}>
          <option value={1}>1</option>
          <option value={5}>5</option>
          <option value={10}>10</option>
          <option value={20}>20</option>
          <option value={30}>30</option>
        </select>
        <button
          type="button"
          disabled={!query.project_id || loadingCount > 0}
          onClick={() => setRevision((value) => value + 1)}
        >
          {loadingCount > 0 ? '조회 중…' : 'Retry'}
        </button>
        {manual && !status && (
          <span role="status" className="query-progress statistics-inline-progress">
            {progressText}
          </span>
        )}
      </div>
      {!manual && !status && <p role="status" className="query-progress">{progressText}</p>}
      {status && (
        <p className="muted" role="status">
          {status}
        </p>
      )}
      <div className="statistics-grid">
        {statisticCards.map(([type, title]) => (
          <StatisticTable
            key={type}
            type={type}
            title={title}
            n={n}
            rows={rows[type] ?? []}
            message={status || messages[type]}
            onSelect={setSelection}
          />
        ))}
      </div>
      {selection && <StatisticDetailDialog selection={selection} query={query} onClose={() => setSelection(null)} />}
    </div>
  )
}
