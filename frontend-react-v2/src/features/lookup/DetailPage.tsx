import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { fetchLogContext, type LogRow } from './service'
export function DetailPage() {
  const [params] = useSearchParams()
  const [context, setContext] = useState<{ before?: LogRow[]; after?: LogRow[]; item?: LogRow }>()
  const [error, setError] = useState('')
  useEffect(() => {
    const projectId = params.get('project_id')
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
  }, [params])
  return (
    <section className="dense-card">
      <h1>Log Detail</h1>
      {error && <p role="alert">{error}</p>}
      {!context && !error && (
        <p className="muted">프로젝트·로그 행을 선택하면 전후 문맥을 표시합니다.</p>
      )}
      {context && (
        <pre style={{ whiteSpace: 'pre-wrap', maxHeight: 480, overflow: 'auto' }}>
          {JSON.stringify(context, null, 2)}
        </pre>
      )}
    </section>
  )
}
