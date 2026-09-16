import { useEffect, useState } from 'react'
import { listAnalysisJobs, type AnalysisJob } from './service'

const phases: Record<string, string> = {
  PREPARING: 'Preparing', READING: 'Reading log', VALIDATING: 'Validating log',
  PARSING: 'Parsing / CSV conversion', COPY: 'Sending CSV to DB', VERIFYING: 'Verifying saved data',
}

export function ParsingProgress({ projectId, runId }: { projectId?: string; runId?: string }) {
  const [elapsed, setElapsed] = useState(0)
  const [jobs, setJobs] = useState<AnalysisJob[]>([])
  const [unavailable, setUnavailable] = useState(false)
  useEffect(() => {
    if (!projectId || !runId) return
    const controller = new AbortController()
    let timer: ReturnType<typeof setTimeout>
    const poll = async () => {
      try {
        const result = await listAnalysisJobs(projectId, runId, controller.signal)
        if (controller.signal.aborted) return
        setJobs(result)
        setUnavailable(false)
      } catch {
        if (controller.signal.aborted) return
        setUnavailable(true)
      }
      if (!controller.signal.aborted) timer = setTimeout(() => void poll(), 1000)
    }
    void poll()
    return () => { controller.abort(); clearTimeout(timer) }
  }, [projectId, runId])
  useEffect(() => {
    const started = Date.now()
    const timer = window.setInterval(() => {
      setElapsed(Math.floor((Date.now() - started) / 1000))
    }, 1000)
    return () => window.clearInterval(timer)
  }, [])

  const duration = `${Math.floor(elapsed / 60)}:${String(elapsed % 60).padStart(2, '0')}`
  const completed = jobs.filter((job) => job.status === 'COMPLETED').length
  const failed = jobs.some((job) => ['FAILED', 'PARTIAL'].includes(job.status))
  const current = jobs.find((job) => job.status === 'PROCESSING' && job.phase) ?? jobs.find((job) => job.status === 'PROCESSING')
  const percent = !unavailable && !failed && current && current.total_units > 0
    ? Math.min(100, Math.floor(current.processed_units / current.total_units * 100)) : undefined
  const label = unavailable ? 'Progress temporarily unavailable; retrying'
    : failed ? 'Processing error; awaiting result'
    : current ? phases[current.phase] ?? 'Waiting to process'
    : jobs.length && completed === jobs.length ? 'Finalizing analysis' : 'Waiting for processing'
  return (
    <div className="parsing-progress">
      <div
        className="parsing-progress-track"
        role="progressbar"
        aria-label="Parsing log files and saving to DB"
        aria-valuenow={percent}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuetext={`${label}${percent === undefined ? '' : `: ${percent}% of current stage`}`}
      >
        <span className="parsing-progress-indicator" style={percent === undefined ? undefined : { width: `${percent}%`, animation: 'none', opacity: 1 }} />
      </div>
      <span className="parsing-progress-caption">{label}{percent === undefined ? '' : ` · ${percent}% (stage)`} · {duration} elapsed</span>
      {jobs.length > 0 && <span className="parsing-progress-caption">Files completed: {completed} / {jobs.length}</span>}
    </div>
  )
}
