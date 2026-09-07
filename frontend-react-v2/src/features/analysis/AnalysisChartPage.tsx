import { useEffect, useMemo, useRef, useState } from 'react'
import ReactECharts from 'echarts-for-react'
import { fetchChartData, fetchStatistics, type AnalysisQuery, type ChartPayload } from './service'

type ChartId = 'tps' | 'request' | 'statusPie' | 'statusBar' | 'visitor' | 'static'
const charts: Array<{ id: ChartId; label: string }> = [
  { id: 'tps', label: 'Transaction Per Second' },
  { id: 'request', label: 'Request (count) / Timetaken' },
  { id: 'statusPie', label: 'HTTP Status Codes' },
  { id: 'statusBar', label: 'Http Status Codes' },
  { id: 'visitor', label: 'Visitor IP top5' },
  { id: 'static', label: 'Static File types' },
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
  return { title: { text: title, left: 'center', top: 6, textStyle: { color: '#46329b', fontSize: 16 } }, legend: { top: 32 }, tooltip: { trigger: 'axis' }, grid: { left: 48, right: 24, top: 72, bottom: 72 }, xAxis: { type: 'category', data: (data?.resultX ?? []).map(formatTimeline) }, yAxis: { type: 'value' }, dataZoom: [{ type: 'inside' }, { type: 'slider', height: 16, bottom: 10 }], series: [{ type: 'line', smooth: true, showSymbol: false, name: time ? 'Time-Taken' : 'TPS', data: time ? data?.resultY_time ?? [] : data?.resultY ?? [] }] }
}
function statusBarOption(data: ChartPayload | null) {
  const x = (data?.resultX ?? []).map(formatTimeline)
  return { title: { text: 'Http Status Codes', left: 'center', top: 6, textStyle: { color: '#46329b', fontSize: 16 } }, tooltip: { trigger: 'axis' }, legend: { top: 32 }, grid: { left: 48, right: 18, top: 72, bottom: 72 }, xAxis: { type: 'category', data: x }, yAxis: { type: 'value' }, dataZoom: [{ type: 'inside' }, { type: 'slider', height: 16, bottom: 10 }], series: [
    { name: '200', type: 'bar', data: data?.resultY_200 ?? [] },
    { name: '300', type: 'bar', data: data?.resultY_300 ?? [] },
    { name: '400', type: 'bar', data: data?.resultY_400 ?? [] },
    { name: '500', type: 'bar', data: data?.resultY_500 ?? [] },
  ] }
}
function pieOption(data: ChartPayload | null, title: string) {
  const rows = (data?.results ?? data?.resultXY ?? []) as Array<Record<string, unknown>>
  const values = rows.map((r) => ({ name: String(r.result ?? r.name ?? r.x ?? '-'), value: Number(r.result_count ?? r.value ?? r.y ?? 0) }))
  return { title: { text: title, left: 'center', top: 6, textStyle: { color: '#46329b', fontSize: 16 } }, tooltip: { trigger: 'item' }, legend: { top: 34, type: 'scroll' }, series: [{ type: 'pie', top: 64, radius: ['35%', '68%'], data: values, label: { formatter: '{b}: {c}' } }] }
}

export function AnalysisChartPage() {
  const initial = useMemo(() => Object.fromEntries(new URLSearchParams(window.location.search)), []) as AnalysisQuery
  const [timeline, setTimeline] = useState(String(initial.type ?? '1'))
  const [query, setQuery] = useState<AnalysisQuery>(initial)
  const [data, setData] = useState<Partial<Record<ChartId, ChartPayload>>>({})
  const [status, setStatus] = useState('Select a timeline and chart to load data.')
  const requestController = useRef<AbortController | null>(null)

  const load = async (id: ChartId, sourceQuery = query, sourceTimeline = timeline) => {
    const params = { ...sourceQuery, type: sourceTimeline, kind: id === 'tps' ? 1 : id === 'request' ? 3 : 2 }
    setStatus('Loading...')
    try {
      const result = id === 'statusPie' || id === 'visitor' || id === 'static'
        ? await fetchStatistics({ ...params, type: id === 'statusPie' ? 1 : id === 'visitor' ? 5 : 9 })
        : await fetchChartData(params)
      setData((current) => ({ ...current, [id]: result }))
      setStatus('')
    } catch { setStatus('Chart API unavailable or parameters are invalid.') }
  }
  const loadAll = async (sourceQuery = query, sourceTimeline = timeline) => {
    requestController.current?.abort()
    const controller = new AbortController()
    requestController.current = controller
    setStatus('Loading charts...')
    const results = await Promise.allSettled(
      charts.map(async (chart) => {
      const params = {
        ...sourceQuery,
        projectServers: Array.isArray(sourceQuery.projectServers)
          ? sourceQuery.projectServers
          : sourceQuery.projectServers
            ? String(sourceQuery.projectServers).split(',').filter(Boolean)
            : [],
        type: sourceTimeline,
          kind: chart.id === 'tps' ? 1 : chart.id === 'request' ? 3 : 2,
        }
        const result =
          chart.id === 'statusPie' || chart.id === 'visitor' || chart.id === 'static'
            ? await fetchStatistics(
                { ...params, type: chart.id === 'statusPie' ? 1 : chart.id === 'visitor' ? 5 : 9 },
                controller.signal,
              )
            : await fetchChartData(params, controller.signal)
        return [chart.id, result] as const
      }),
    )
    if (controller.signal.aborted) return
    const successful = results.filter(
      (result): result is PromiseFulfilledResult<readonly [ChartId, ChartPayload]> =>
        result.status === 'fulfilled',
    )
    setData((current) => ({ ...current, ...Object.fromEntries(successful.map((result) => result.value)) }))
    setStatus(successful.length === charts.length ? '' : 'Some charts could not be loaded.')
  }
  useEffect(() => {
    const handler = (event: Event) => {
      const detail = (event as CustomEvent<AnalysisQuery>).detail
      const nextTimeline = String(detail.type ?? '1')
      setQuery(detail)
      setTimeline(nextTimeline)
      void loadAll(detail, nextTimeline)
    }
    window.addEventListener('elao:analysis-search', handler)
    return () => {
      window.removeEventListener('elao:analysis-search', handler)
      requestController.current?.abort()
    }
    // The loader intentionally uses the latest event payload and is not a hook dependency.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
  const refreshAll = () => { void loadAll() }
  return <div className="chart-workspace">
    <div className="chart-filters">
      <div className="chart-filter-row"><strong>Timeline</strong>{[['1', 'HH'], ['2', 'HHMM'], ['3', 'HHMMSS']].map(([value, label]) => <label className="inline-check" key={value}><input type="radio" name="timeline" checked={timeline === value} onChange={() => setTimeline(value)} />{label}</label>)}</div>
      <div className="chart-filter-row"><strong>Charts</strong>{charts.map((chart) => <button type="button" key={chart.id} className="chart-selector" onClick={() => void load(chart.id)}>{chart.label}</button>)}<button type="button" onClick={refreshAll}>ALL</button></div>
    </div>
    {status && <p role="status" className="muted">{status}</p>}
    <div className="chart-grid">{charts.map((chart) => {
      const chartData = data[chart.id] ?? null
      const option = chart.id === 'tps' ? lineOption(chartData, chart.label) : chart.id === 'request' ? lineOption(chartData, chart.label, true) : chart.id === 'statusBar' ? statusBarOption(chartData) : pieOption(chartData, chart.label)
      return <div className="chart-card" key={chart.id}><ReactECharts option={option} style={{ height: 330 }} notMerge lazyUpdate /></div>
    })}</div>
  </div>
}

const statisticCards = [
  [2, 'Requests URI (count)'], [5, 'Visitors (count)'], [4, 'Requests Time-taken (s/µs)'],
  [1, 'HTTP Status Codes (count)'], [8, 'Requests URI (Total Bytes)'], [6, 'Referers (count)'],
  [12, 'Static file names (count)'], [13, 'Upstream Info (count)'], [14, 'Domains (count, K8S Ingress)'],
  [11, 'Requests URI (Average Bytes)'], [3, '404 Requests URI (count)'], [10, 'Requests Average Time-taken (s/µs)'],
  [7, 'User Agent (count)'], [9, 'Static files (count)'],
] as const

type StatisticRow = { result?: unknown; result_count?: unknown; result_per?: unknown }

function StatisticTable({ title, rows, n }: { title: string; rows: StatisticRow[]; n: number }) {
  const display = Array.from({ length: n }, (_, index) => rows[index] ?? {})
  return <div className="statistic-table-wrap"><h3 className="statistic-table-title">{title}</h3><table className="statistic-table"><thead><tr><th>Top {n}</th><th>{title}</th><th>Result</th></tr></thead><tbody>{display.map((row, index) => <tr key={index}><td>{index + 1}</td><td>{String(row.result ?? '-')}</td><td>{String(row.result_count ?? 0)}{row.result_per !== undefined && <small> ({Number(row.result_per).toFixed(2)}%)</small>}</td></tr>)}</tbody></table></div>
}

export function StatisticsPage() {
  const [n, setN] = useState(5)
  const [query, setQuery] = useState<AnalysisQuery>({})
  const [rows, setRows] = useState<Record<number, StatisticRow[]>>({})
  const [status, setStatus] = useState('Run Search to load statistics.')
  const load = async (sourceQuery: AnalysisQuery, topN: number) => {
    setStatus('Loading statistics...')
    const results = await Promise.allSettled(statisticCards.map(async ([type]) => [type, await fetchStatistics({ ...sourceQuery, type, N: topN })] as const))
    const next: Record<number, StatisticRow[]> = {}
    results.forEach((result) => { if (result.status === 'fulfilled') next[result.value[0]] = (result.value[1].results ?? []) as StatisticRow[] })
    setRows(next)
    setStatus(Object.keys(next).length ? '' : 'Statistics API unavailable or parameters are invalid.')
  }
  useEffect(() => {
    const handler = (event: Event) => { const detail = (event as CustomEvent<AnalysisQuery>).detail; setQuery(detail); void load(detail, n) }
    window.addEventListener('elao:analysis-search', handler)
    return () => window.removeEventListener('elao:analysis-search', handler)
  }, [n])
  const changeN = (value: number) => { setN(value); if (query.project_id) void load(query, value) }
  return <div className="statistics-workspace"><div className="statistics-controls"><strong>Select N</strong><select value={n} onChange={(event) => changeN(Number(event.target.value))}><option value={1}>1</option><option value={5}>5</option><option value={10}>10</option></select></div>{status && <p className="muted" role="status">{status}</p>}<div className="statistics-grid">{statisticCards.map(([type, title]) => <StatisticTable key={type} title={title} n={n} rows={rows[type] ?? []} />)}</div></div>
}
