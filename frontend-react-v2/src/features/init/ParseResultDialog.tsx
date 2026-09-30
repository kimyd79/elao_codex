import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import type { ParseResult } from './service'

export function ParseResultDialog({ result, onClose, onContinue }: {
  result: ParseResult; onClose: () => void
  onContinue: (onProgress: (text: string) => void) => Promise<void>
}) {
  const dialog = useRef<HTMLDialogElement>(null)
  const busy = useRef(false)
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState('')
  const [error, setError] = useState('')
  const completed = result.status === 'COMPLETED'
  const rate = result.source_count ? result.rejected_count / result.source_count * 100 : 0
  useEffect(() => {
    const element = dialog.current!
    element.showModal()
    return () => element.close()
  }, [])
  const proceed = async () => {
    if (busy.current || !completed) return
    busy.current = true
    setLoading(true)
    setError('')
    try { await onContinue(setProgress) }
    catch (error) { setError(error instanceof Error ? error.message : '분석 데이터를 불러오지 못했습니다. 다시 시도해 주세요.') }
    finally { busy.current = false; setLoading(false) }
  }
  return createPortal(
    <dialog ref={dialog} className="dense-card parse-result-dialog" aria-labelledby="parse-result-title"
      onCancel={(event) => { event.preventDefault(); if (!busy.current) onClose() }}>
      <h2 id="parse-result-title">{completed ? '로그 처리 완료' : '로그 처리 실패'}</h2>
      <div className="parse-result-counts">
        <div>전체 로그<strong>{result.source_count.toLocaleString()}건</strong></div>
        <div>저장 완료<strong>{result.stored_count.toLocaleString()}건</strong></div>
        <div>파싱 오류 / 누락<strong>{result.rejected_count.toLocaleString()}건</strong><span>전체 대비 {rate.toLocaleString(undefined, { maximumFractionDigits: 6 })}%</span></div>
      </div>
      <p>{completed
        ? result.rejected_count ? '오류 비율이 1% 미만이므로 정상 로그는 저장되었습니다. 아래 내용을 확인한 뒤 다음 단계 진행 여부를 선택하세요.' : '모든 로그가 정상 저장되었습니다. 다음 단계로 진행하면 분석 데이터를 불러옵니다.'
        : '정상 완료 기준을 충족하지 못해 이번 처리 데이터는 저장되지 않았습니다. 오류를 확인하고 다시 처리해 주세요.'}</p>
      {result.files.filter((file) => (file.rejected_count ?? 0) > 0 || file.failure_reasons?.length).map((file) => (
        <section className="parse-result-file" key={file.logfile_id}>
          <h3>{file.file_name ?? file.logfile_id}</h3>
          <ul>{file.failure_reasons?.map((reason) => (
            <li key={`${reason.error_code}-${reason.error_message}`}><b>{reason.count.toLocaleString()}건 · {reason.error_code === 'invalid_nul' ? 'NUL 제어문자 포함' : reason.error_code}</b> — {reason.error_message}</li>
          ))}</ul>
          <p className="muted">실패 로그 일부 (파일당 최대 5건, 긴 로그는 앞뒤 일부만 표시)</p>
          {file.failure_samples?.map((sample) => (
            <div key={sample.line_number} className="parse-result-sample">
              <b>{sample.line_number.toLocaleString()}번째 줄 · {sample.error_message}</b>
              <pre>{sample.raw_line_excerpt}</pre>
            </div>
          ))}
          {!file.failure_samples?.length && <p>해당 누락 건의 원문 위치는 기록되지 않았습니다.</p>}
        </section>
      ))}
      {loading && <p role="status" aria-live="polite">{progress || '분석 데이터 로딩 중…'}</p>}
      {error && <p role="alert">데이터 로딩 실패: {error} 다시 시도하거나 현재 단계에 머물 수 있습니다.</p>}
      <div className="wizard-actions">
        <button type="button" disabled={loading} onClick={onClose}>현재 단계에 머물기</button>
        <button type="button" disabled={loading || !completed} onClick={() => void proceed()}>{loading ? '데이터 로딩 중…' : '처리 완료하고 다음 단계'}</button>
      </div>
    </dialog>, document.body,
  )
}
