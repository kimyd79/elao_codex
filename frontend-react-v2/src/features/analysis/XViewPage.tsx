import { useEffect, useMemo, useState } from 'react'
import ReactECharts from 'echarts-for-react'
import { useSearchParams } from 'react-router-dom'
import { Search } from './AnalysisWorkspacePage'
import { fetchXView, type AnalysisQuery, type XViewPayload } from './service'
import { formatAxisTimestamp, timelineTimestamp } from './timelineChart'
import { XViewDetailDialog } from './XViewDetailDialog'
import type { XViewBounds } from './service'

const statusGroups = [
  { key: '20x', label: '20x Success', color: '#2563eb' },
  { key: '30x', label: '30x Redirect', color: '#38bdf8' },
  { key: '40x', label: '40x Client error', color: '#f59e0b' },
  { key: '50x', label: '50x Server error', color: '#ef4444' },
  { key: 'other', label: 'Other', color: '#94a3b8' },
] as const

type ScatterDatum = [number, number]

function buildXViewOption(data: XViewPayload | null) {
  const points = data?.points ?? []
  return {
    animation: false,
    color: statusGroups.map((group) => group.color),
    tooltip: { show: false, triggerOn: 'none' },
    legend: { top: 8, left: 'center', selectedMode: false },
    toolbox: {
      right: 14,
      top: 4,
      feature: {
        brush: { type: ['rect', 'clear'] },
        dataZoom: { xAxisIndex: 0, yAxisIndex: 0, title: { zoom: 'Zoom', back: 'Zoom reset' } },
      },
    },
    brush: { toolbox: ['rect', 'clear'], seriesIndex: [], xAxisIndex: 0, yAxisIndex: 0, brushType: 'rect', brushMode: 'single', transformable: false },
    grid: { left: 24, right: 84, top: 64, bottom: 66, containLabel: true },
    xAxis: {
      type: 'time',
      name: 'Time',
      nameLocation: 'end',
      axisLabel: { formatter: (value: number) => formatAxisTimestamp(value), hideOverlap: true },
      splitLine: { show: true, lineStyle: { color: '#edf0f6' } },
    },
    yAxis: {
      type: 'value',
      position: 'right',
      name: 'Response time (ms)',
      nameLocation: 'end',
      min: 0,
      splitLine: { lineStyle: { color: '#e8ecf4' } },
    },
    series: statusGroups.map((group) => ({
      name: group.label,
      type: 'scatter',
      silent: true,
      emphasis: { disabled: true },
      symbol: 'circle',
      symbolSize: 5,
      itemStyle: { color: group.color, opacity: .72 },
      large: true,
      largeThreshold: 2_000,
      // Brush updateVisual renders synchronously using the current point layout.
      // Progressive layouts only contain the last chunk, which drops earlier
      // points on selection. Keep large-mode batching, but lay out every point.
      progressive: 0,
      data: points
        .filter((point) => point.status_group === group.key)
        .map((point): ScatterDatum | null => {
          const timestamp = timelineTimestamp(point.time)
          return timestamp === null ? null : [timestamp, point.response_time_ms]
        })
        .filter((point): point is ScatterDatum => point !== null),
    })),
  }
}

export function XViewPage() {
  const [params] = useSearchParams()
  const projectId = params.get('project_id') ?? ''
  const [query, setQuery] = useState<AnalysisQuery | null>(null)
  const [data, setData] = useState<XViewPayload | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedUri, setSelectedUri] = useState<string | null>(null)
  const [bounds, setBounds] = useState<XViewBounds | null>(null)
  const activeQuery = useMemo<AnalysisQuery | null>(() => query ? { ...query, xview_uri: selectedUri ?? undefined } : null, [query, selectedUri])
  const option = useMemo(() => buildXViewOption(data), [data])
  const maxUriCount = Math.max(1, ...(data?.uris ?? []).map((item) => item.count))

  useEffect(() => {
    if (!activeQuery?.project_id) return
    const controller = new AbortController()
    setLoading(true)
    setError('')
    void fetchXView(activeQuery, controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) {
          setData(result)
          if (result.limit_exceeded) setError(result.message ?? '조회 데이터가 100만 건을 초과합니다. 검색조건을 설정하여 조회 데이터를 줄여 주세요.')
        }
      })
      .catch((reason: unknown) => {
        if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : 'X-View 조회에 실패했습니다.')
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false)
      })
    return () => controller.abort()
  }, [activeQuery])

  const onBrushEnd = (event: { areas?: Array<{ coordRange?: number[][] }> }) => {
    if (loading) return
    const range = event.areas?.[0]?.coordRange
    if (!range || range.length !== 2) return
    const start = Math.ceil(Math.min(...range[0]) / 1000) * 1000
    const end = Math.floor(Math.max(...range[0]) / 1000) * 1000
    if (start > end) return
    const stamp = (time: number) => formatAxisTimestamp(time).replace(/\D/g, '')
    setBounds({ start: stamp(start), end: stamp(end), lower: Math.max(0, Math.min(...range[1])), upper: Math.max(0, ...range[1]) })
  }

  return (
    <section className="dense-card analysis-workspace xview-workspace">
      <div className="analysis-heading">
        <div>
          <p className="auth-kicker" style={{ color: '#5269d4' }}>REQUEST DISTRIBUTION</p>
          <h1 className="analysis-title">X-View</h1>
          <p className="muted">요청 시각과 응답 소요시간의 분포를 URI와 HTTP 상태별로 확인합니다.</p>
        </div>
      </div>
      {!projectId && <p role="status">Initialization에서 분석할 프로젝트를 선택하세요.</p>}
      {projectId && <Search projectId={projectId} targetPath="/x-view" onSearch={(next) => { setBounds(null); setSelectedUri(null); setQuery(next as AnalysisQuery) }} />}
      {error && <p className="statistic-detail-error" role="alert">{error}</p>}
      <div className="xview-summary" role="status">
        {loading ? 'X-View 데이터 조회 중…' : data ? `전체 ${data.total_count.toLocaleString()}건 · 표시 ${data.displayed_count.toLocaleString()}건` : 'Search 조건으로 조회하면 X-View가 표시됩니다.'}
      </div>
      <div className="xview-panel query-region" aria-busy={loading}>
        <aside className="xview-uri-list" aria-label="URI call counts">
          <div className="xview-uri-heading"><strong>URI</strong><strong>Calls</strong></div>
          {(data?.uris ?? []).map((item) => (
            <button type="button" className="xview-uri-item" key={item.uri} title={item.uri} aria-pressed={selectedUri === item.uri} onClick={() => { setBounds(null); setSelectedUri((current) => current === item.uri ? null : item.uri) }}>
              <div><span>{item.uri}</span><strong>{item.count.toLocaleString()}</strong></div>
              <i style={{ width: `${Math.max(3, (item.count / maxUriCount) * 100)}%` }} />
            </button>
          ))}
          {data && !data.uris.length && <p className="muted">조회된 URI가 없습니다.</p>}
        </aside>
        <div className="xview-chart">
          <ReactECharts key={data ? `${selectedUri ?? 'all'}-${JSON.stringify(query)}` : 'empty'} option={option} style={{ width: '100%', height: '100%' }} autoResize notMerge lazyUpdate onEvents={{ brushEnd: onBrushEnd }} onChartReady={(chart) => chart.dispatchAction({ type: 'takeGlobalCursor', key: 'brush', brushOption: { brushType: 'rect', brushMode: 'single' } })} />
        </div>
        {loading && <div className="query-overlay"><span className="query-loading" role="status"><span className="query-spinner" aria-hidden="true" />데이터 조회 중…</span></div>}
      </div>
      <p className="muted">URL을 다시 선택하면 전체 조회로 돌아갑니다. 차트에서 영역을 드래그하면 해당 시간·응답시간 범위의 로그를 조회합니다.</p>
      {bounds && activeQuery && <XViewDetailDialog query={activeQuery} bounds={bounds} onClose={() => setBounds(null)} />}
    </section>
  )
}
