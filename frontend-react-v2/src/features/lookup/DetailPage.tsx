import { useSearchParams } from 'react-router-dom'
import { useCallback, useEffect, useState } from 'react'
import { fetchLogs, fetchLogContext, type LogRow } from './service'
import { Search } from '@/features/analysis/AnalysisWorkspacePage'
import { AgGridReact } from 'ag-grid-react'
import { AllCommunityModule, ModuleRegistry, type ColDef } from 'ag-grid-community'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-quartz.css'
ModuleRegistry.registerModules([AllCommunityModule])
export function DetailPage() {
  const [params] = useSearchParams()
  const [context, setContext] = useState<{ before?: LogRow[]; after?: LogRow[]; item?: LogRow }>()
  const [error, setError] = useState('')
  const [rows, setRows] = useState<LogRow[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [pageSize, setPageSize] = useState(20)
  const [page, setPage] = useState(1)
  const [activeQuery, setActiveQuery] = useState<Record<string, unknown>>({})
  const [selectedRow, setSelectedRow] = useState<LogRow | null>(null)
  const projectId = params.get('project_id') ?? ''
  const load = useCallback(async (next: Record<string, unknown>, targetPage = 1) => {
    if (!projectId) return
    setLoading(true); setError('')
    try {
      const result = await fetchLogs({ projectId, limit: pageSize, offset: (targetPage - 1) * pageSize, condition: String(next.conditionValue ?? ''), search: String(next.searchValue ?? ''), excludeSearch: String(next.excludeSearch) === 'true', dateFrom: next.dateFromValue ? String(next.dateFromValue) : undefined, dateTo: next.dateToValue ? String(next.dateToValue) : undefined, timeFrom: next.timeFromValue ? String(next.timeFromValue) : undefined, timeTo: next.timeToValue ? String(next.timeToValue) : undefined, ttFrom: next.ttFromValue ? String(next.ttFromValue) : undefined, ttTo: next.ttToValue ? String(next.ttToValue) : undefined, server: Array.isArray(next.projectServers) ? next.projectServers.join(',') : String(next.projectServers ?? '') })
      setPage(targetPage)
      setRows(result.results ?? result.items ?? []); setTotal(result.count ?? (result.results ?? result.items ?? []).length)
    } catch (reason) { setError(reason instanceof Error ? reason.message : 'Detail query failed.') }
    finally { setLoading(false) }
  }, [pageSize, projectId])
  const formatDate = (value: unknown) => {
    const text = String(value ?? '').replace(/[^0-9]/g, '')
    return text.length === 8 ? `${text.slice(0, 4)}/${text.slice(4, 6)}/${text.slice(6, 8)}` : String(value ?? '-')
  }
  const formatTime = (value: unknown) => {
    const text = String(value ?? '').replace(/[^0-9]/g, '').padStart(6, '0')
    return text.length === 6 ? `${text.slice(0, 2)}:${text.slice(2, 4)}:${text.slice(4, 6)}` : String(value ?? '-')
  }
  const formatNumber = (value: unknown) => {
    const number = Number(value)
    return Number.isFinite(number) ? number.toLocaleString() : '-'
  }
  const columns = useState<ColDef<LogRow>[]>([
    { field: 'fdate', headerName: 'Date', width: 120, valueFormatter: (params) => formatDate(params.value) }, { field: 'ftime', headerName: 'Time', width: 110, valueFormatter: (params) => formatTime(params.value) },
    { field: 'fip', headerName: 'IP', width: 150 }, { field: 'frequest', headerName: 'Request', flex: 1, minWidth: 280 },
    { field: 'freferer', headerName: 'Referrer', flex: 1, minWidth: 160 }, { field: 'fuser_agent', headerName: 'UserAgent', flex: 1, minWidth: 160 },
    { field: 'fstatus', headerName: 'Status', width: 90 }, { field: 'fbyte', headerName: 'Byte', width: 110, type: 'numericColumn', cellStyle: { textAlign: 'right' }, valueFormatter: (params) => formatNumber(params.value) }, { field: 'ftime_taken', headerName: 'TimeTaken (μs)', width: 140, type: 'numericColumn', cellStyle: { textAlign: 'right' }, valueFormatter: (params) => formatNumber(params.value) },
  ])[0]
  useEffect(() => {
    if (!projectId) return
    const controller = new AbortController()
    void fetchLogContext(
      {
        project_id: projectId,
        logfile_id: params.get('logfile_id') ?? undefined,
        line_no: Number(params.get('line_no') ?? 0),
        before: 3,
        after: 3,
      },
      controller.signal,
    )
      .then(setContext)
      .catch((reason: Error) => {
        if (reason.name !== 'CanceledError') setError('상세 문맥을 조회하지 못했습니다.')
      })
    return () => controller.abort()
  }, [params, projectId])
  useEffect(() => {
    if (projectId && rows.length) void load(activeQuery, 1)
    // Refresh the current result set when the requested page size changes.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pageSize])
  const totalPages = Math.max(1, Math.ceil(total / pageSize))
  const pageItems = Array.from(new Set([1, page - 2, page - 1, page, page + 1, page + 2, totalPages].filter((value) => value >= 1 && value <= totalPages)))
  const pageInputWidth = Math.max(64, String(totalPages).length * 8 + 42)
  return (
    <section className="dense-card lookup-workspace">
      <div className="analysis-heading">
        <div>
          <p className="auth-kicker" style={{ color: '#5269d4' }}>LOG DETAIL</p>
          <h1 className="analysis-title">Detail</h1>
          <p className="muted">Review the selected log line with surrounding entries.</p>
        </div>
      </div>
      <Search projectId={projectId} targetPath="/detail" onSearch={(next) => { setActiveQuery(next); setPage(1); void load(next, 1) }} />
      {error && <p role="alert">{error}</p>}
      {!context && !error && (
        <p className="muted">프로젝트·로그 행을 선택하면 전후 문맥을 표시합니다.</p>
      )}
      {context && (
        <div className="detail-context-table">
          <table className="statistic-table">
            <thead><tr><th>Position</th><th>Line</th><th>Log</th></tr></thead>
            <tbody>
              {(context.before ?? []).map((row, index) => (
                <tr key={`before-${index}`}><td>Before</td><td>{String(row.line_no ?? '-')}</td><td><code>{String(row.raw_log ?? row.log_line ?? '-')}</code></td></tr>
              ))}
              {context.item && <tr className="detail-selected-row"><td>Selected</td><td>{String(context.item.line_no ?? '-')}</td><td><code>{String(context.item.raw_log ?? context.item.log_line ?? '-')}</code></td></tr>}
              {(context.after ?? []).map((row, index) => (
                <tr key={`after-${index}`}><td>After</td><td>{String(row.line_no ?? '-')}</td><td><code>{String(row.raw_log ?? row.log_line ?? '-')}</code></td></tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <section className="detail-results"><div className="detail-table-toolbar"><strong>Total {total.toLocaleString()}</strong><label>Rows <select value={pageSize} onChange={(event) => { const size = Number(event.target.value); setPageSize(size); setPage(1) }}><option value={20}>20</option><option value={30}>30</option><option value={50}>50</option><option value={100}>100</option></select></label></div><div className="ag-theme-quartz detail-grid-auto" style={{ width: '100%', marginTop: 12 }}><AgGridReact rowData={rows} columnDefs={columns} loading={loading} domLayout="autoHeight" onRowClicked={(event) => { const row = event.data; if (row) { setSelectedRow(row); if (projectId) { const line = Number(row.line_no ?? row.id ?? 0); void fetchLogContext({ project_id: projectId, logfile_id: row.logfile_id, line_no: line, before: 3, after: 3 }).then(setContext).catch(() => undefined) } } }} /></div><div className="detail-pagination"><button type="button" disabled={loading || page <= 1} onClick={() => void load(Object.fromEntries(params.entries()), page - 1)}>Previous</button><span>Page {page} of {Math.max(1, Math.ceil(total / pageSize))}</span><button type="button" disabled={loading || page >= Math.ceil(total / pageSize)} onClick={() => void load(Object.fromEntries(params.entries()), page + 1)}>Next</button></div></section>
      <div className="detail-pagination detail-pagination-image"><button type="button" className="page-arrow" disabled={loading || page <= 1} onClick={() => void load(activeQuery, page - 1)} aria-label="Previous page">‹</button>{pageItems.map((item, index) => <span key={item}>{index > 0 && item > pageItems[index - 1] + 1 && <span className="page-ellipsis">...</span>}<button type="button" className={item === page ? 'page-number active' : 'page-number'} disabled={loading || item === page} onClick={() => void load(activeQuery, item)}>{item}</button></span>)}<button type="button" className="page-arrow" disabled={loading || page >= totalPages} onClick={() => void load(activeQuery, page + 1)} aria-label="Next page">›</button><label className="page-go"><input type="number" min={1} max={totalPages} defaultValue={page} key={page} style={{ width: pageInputWidth }} aria-label={`Page number, maximum ${totalPages}`} onKeyDown={(event) => { if (event.key === 'Enter') { const value = Math.min(totalPages, Math.max(1, Number(event.currentTarget.value))); void load(activeQuery, value) } }} /><button type="button" onClick={(event) => { const input = event.currentTarget.previousElementSibling as HTMLInputElement; const value = Math.min(totalPages, Math.max(1, Number(input.value))); void load(activeQuery, value) }}>GO</button></label></div>
      {selectedRow && <div className="detail-row-backdrop" role="presentation" onClick={() => setSelectedRow(null)}>
        <section className="detail-row-dialog" role="dialog" aria-modal="true" aria-labelledby="detail-row-title" onClick={(event) => event.stopPropagation()}>
          <div className="detail-dialog-heading"><h2 id="detail-row-title">Log Detail</h2><button type="button" className="detail-close-button" onClick={(event) => { event.stopPropagation(); setSelectedRow(null) }}>Close</button></div>
          <table className="detail-fields-table"><tbody>{Object.entries(selectedRow).map(([key, value]) => <tr key={key}><th>{key}</th><td>{String(value ?? '-')}</td></tr>)}</tbody></table>
        </section>
      </div>}
    </section>
  )
}
