import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import { fetchXViewDetails, type AnalysisQuery, type XViewBounds } from './service'

const columns = [
  ['fdate', 'Date'], ['ftime', 'Time'], ['fip', 'IP'], ['frequest', 'Request'],
  ['fstatus', 'Status'], ['fbyte', 'Byte'], ['xview_ms', 'TimeTaken (ms)'],
]

function display(key: string, value: string | number) {
  const text = String(value ?? '-')
  if (key === 'fdate' && /^\d{8}$/.test(text)) return `${text.slice(0, 4)}/${text.slice(4, 6)}/${text.slice(6)}`
  if (key === 'ftime' && /^\d{6}$/.test(text)) return `${text.slice(0, 2)}:${text.slice(2, 4)}:${text.slice(4)}`
  if (key === 'fbyte' || key === 'xview_ms') return Number(value).toLocaleString(undefined, { maximumFractionDigits: 3 })
  return text
}

export function XViewDetailDialog({ query, bounds, onClose }: { query: AnalysisQuery; bounds: XViewBounds; onClose: () => void }) {
  const [page, setPage] = useState(1)
  const [ordering, setOrdering] = useState('fdatetime')
  const [data, setData] = useState<{ count: number; results: Array<Record<string, string | number>> }>({ count: 0, results: [] })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const dialog = useRef<HTMLDialogElement>(null)
  const totalPages = Math.max(1, Math.ceil(data.count / 20))
  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError('')
    void fetchXViewDetails(query, bounds, page, controller.signal, ordering).then((result) => {
      if (!controller.signal.aborted) setData(result)
    }).catch((reason: unknown) => {
      if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : '조회에 실패했습니다.')
    }).finally(() => { if (!controller.signal.aborted) setLoading(false) })
    return () => controller.abort()
  }, [query, bounds, page, ordering])
  useEffect(() => { dialog.current?.showModal() }, [])
  const stamp = (value: string) => `${display('fdate', value.slice(0, 8))} ${display('ftime', value.slice(8))}`
  return createPortal(
    <dialog ref={dialog} className="statistic-detail-dialog xview-detail-dialog" onCancel={onClose} aria-labelledby="xview-detail-title">
      <header className="statistic-detail-header">
        <div><h2 id="xview-detail-title">X-View · 선택 영역 상세 로그</h2>
          <p>{stamp(bounds.start)} ~ {stamp(bounds.end)} · {bounds.lower.toLocaleString()} ~ {bounds.upper.toLocaleString()} ms</p>
          <p>URL: {String(query.xview_uri ?? '전체')} · 기존 Search 조건 적용</p>
        </div><button type="button" onClick={onClose}>Close</button>
      </header>
      <section className="statistic-detail-section" aria-busy={loading}>
        <p role="status">{loading ? '로그 조회 중…' : `Total ${data.count.toLocaleString()}`}</p>
        {error && <p role="alert" className="statistic-detail-error">{error}</p>}
        <div style={{ overflowX: 'auto' }}><table className="statistic-table xview-detail-table">
          <thead><tr>{columns.map(([key, title]) => <th key={key} aria-sort={ordering === key ? 'ascending' : ordering === `-${key}` ? 'descending' : 'none'}>
            <button type="button" className="xview-sort" onClick={() => { setPage(1); setOrdering(ordering === key ? `-${key}` : key) }}>{title}<span aria-hidden="true">{ordering === key ? ' ▲' : ordering === `-${key}` ? ' ▼' : ' ↕'}</span></button>
          </th>)}</tr></thead>
          <tbody>{!loading && !data.results.length && <tr><td colSpan={columns.length}>조회된 로그가 없습니다.</td></tr>}
            {data.results.map((row) => <tr key={row.id}>{columns.map(([key]) => <td key={key} style={{ textAlign: ['fbyte', 'xview_ms'].includes(key) ? 'right' : 'left' }}>{display(key, row[key])}</td>)}</tr>)}
          </tbody>
        </table></div>
        <div className="detail-pagination detail-pagination-image">
          <button disabled={loading || page <= 1} onClick={() => setPage(page - 1)}>‹</button>
          <span>{page} / {totalPages}</span>
          <button disabled={loading || page >= totalPages} onClick={() => setPage(page + 1)}>›</button>
        </div>
      </section>
    </dialog>, document.body,
  )
}
