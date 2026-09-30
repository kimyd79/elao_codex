import { useEffect, useRef, useState } from 'react'
import { apiRequest } from '@/lib/api/client'
import type { AnalysisQuery } from './service'
import type { PreparedAnalysis } from './prepareAnalysis'
import './findings.css'

type EvidenceRow = Record<string, string | number | null>
type Finding = {
  id: string; title: string; status: 'detected' | 'clear' | 'insufficient'
  rule: string; guidance: string[]
  evidence: Record<string, number | null | EvidenceRow[]>
}
export type FindingsResult = {
  total: number; scope: { start: string; end: string; bucket_seconds: number }
  findings: Finding[]; limitations: string[]
}
const labels: Record<string, string> = {
  count: '건수', rate: '비율 (%)', avg_ms: '평균 (ms)', max_ms: '최대 (ms)', p95_ms: 'p95 (ms)', p99_ms: 'p99 (ms)',
  slow: '1초 이상 요청', excluded: '성능 분석 제외 건수', spikes: '트래픽 급증 구간', spike_count: '급증 구간 수',
  concentrated_ips: '집중 IP', concentrated_requests: '집중 요청', top_ips: '상위 IP', top_requests: '상위 요청', slow_urls: '느린 요청',
  latency_changes: '평균 응답시간 증가 구간 (ms)', latency_change_count: '지연 증가 구간 수',
  increases: '비율 증가 구간 (기준·관측값: 0~1)', increase_count: '비율 증가 구간 수', top_urls: '상위 요청', referrers: '404 요청·Referer',
  fip: 'IP', frequest: '요청', fstatus: '상태코드', freferer: 'Referer', share: '점유율 (%)',
  start: '시작', end: '종료 (미포함)', baseline: '직전 구간 중앙값', observed: '관측값',
}
function valueText(value: string | number | null) {
  if (value === null) return '측정값 없음'
  return typeof value === 'number' ? value.toLocaleString(undefined, { maximumFractionDigits: 3 }) : value
}
function Evidence({ evidence }: { evidence: Finding['evidence'] }) {
  return <div className="finding-evidence">{Object.entries(evidence).map(([key, value]) =>
    Array.isArray(value) ? value.length > 0 && <details key={key}>
      <summary>{labels[key] ?? key} ({value.length})</summary>
      <div className="finding-table"><table><thead><tr>{Object.keys(value[0]).map((column) =>
        <th key={column}>{labels[column] ?? column}</th>)}</tr></thead><tbody>{value.map((row, i) =>
        <tr key={i}>{Object.keys(value[0]).map((column) => <td key={column}>{valueText(row[column])}</td>)}</tr>
      )}</tbody></table></div>
    </details> : <span className="finding-metric" key={key}>{labels[key] ?? key}: <b>{valueText(value)}</b></span>,
  )}</div>
}

export function Findings({ projectId, initial }: { projectId: string; initial?: PreparedAnalysis }) {
  const [query, setQuery] = useState<AnalysisQuery>(initial?.query ?? { project_id: projectId })
  const [revision, setRevision] = useState(0)
  const [result, setResult] = useState<FindingsResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const sequence = useRef(0)
  useEffect(() => {
    const handler = (event: Event) => {
      const next = (event as CustomEvent<AnalysisQuery>).detail
      if (next.project_id && next.project_id !== projectId) return
      setQuery(next)
    }
    window.addEventListener('elao:analysis-search', handler)
    return () => window.removeEventListener('elao:analysis-search', handler)
  }, [projectId])
  useEffect(() => {
    if (!projectId) return
    const id = ++sequence.current
    const controller = new AbortController()
    setLoading(true)
    setError('')
    setResult(null)
    const { project_id: ignoredProject, ...filter } = query
    void ignoredProject
    void apiRequest<FindingsResult>({ method: 'POST', url: '/logdetail_dynamic/operational_findings/',
      data: { project_id: projectId, filter }, signal: controller.signal, timeout: 120_000,
    }).then((response) => {
      if (!controller.signal.aborted && id === sequence.current) setResult(response)
    }).catch(() => {
      if (!controller.signal.aborted && id === sequence.current) setError('분석 결과를 불러오지 못했습니다. 접근 권한·로그 분석 완료 여부를 확인하거나 범위를 줄여 다시 시도하세요.')
    }).finally(() => {
      if (!controller.signal.aborted && id === sequence.current) setLoading(false)
    })
    return () => controller.abort()
  }, [projectId, query, revision])
  return <section className="analysis-panel" aria-label="Analysis Finding" aria-busy={loading}>
    <div className="finding-heading"><h2>Analysis Finding</h2>
      <button disabled={!projectId || loading} onClick={() => setRevision((n) => n + 1)}>다시 분석</button></div>
    {!projectId && <p>프로젝트를 선택하세요.</p>}
    {loading && <p role="status">4개 항목 분석 중…</p>}
    {error && <p role="alert">{error}</p>}
    {result && <>
      <p>{result.scope.start} ~ {result.scope.end} · {result.total.toLocaleString()}건 · 구간 {result.scope.bucket_seconds}초</p>
      <p className="muted">Search 조건을 적용합니다. 최초 진입 시 프로젝트 전체 또는 준비된 분석 범위를 사용합니다.</p>
      {!result.total && <p role="status">선택 조건에 해당하는 로그가 없습니다.</p>}
      <div className="finding-grid">{result.findings.map((finding) => <article className="finding-card" key={finding.id}>
        <div className="finding-heading"><h3>{finding.title}</h3><span className={`finding-status ${finding.status}`}>
          {{ detected: '확인 필요', clear: '기준 해당 없음', insufficient: '분석 데이터 부족' }[finding.status]}</span></div>
        <p>{finding.rule}</p>
        <Evidence evidence={finding.evidence} />
        <h4>확인 및 조치 가이드</h4><ol>{finding.guidance.map((guide) => <li key={guide}>{guide}</li>)}</ol>
      </article>)}</div>
      <details><summary>분석 기준과 한계</summary><ul>{result.limitations.map((item) => <li key={item}>{item}</li>)}</ul></details>
    </>}
  </section>
}
