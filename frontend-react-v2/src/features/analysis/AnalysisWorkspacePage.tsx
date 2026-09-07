import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { AnalysisChartPage, StatisticsPage } from './AnalysisChartPage'
import { apiRequest } from '@/lib/api/client'
import {
  listLogFiles,
  listProjects,
  type LogFileSummary,
  type ProjectSummary,
} from '@/features/init/service'
import { fetchPeriod } from './service'

export function AnalysisWorkspacePage() {
  const [params] = useSearchParams()
  const projectId = params.get('project_id') ?? ''
  return (
    <section className="dense-card analysis-workspace">
      <div className="workspace-heading">
        <div>
          <p className="auth-kicker" style={{ color: '#5269d4' }}>
            ANALYSIS WORKSPACE
          </p>
          <h1>Analysis</h1>
          <p className="muted">
            Explore project information, findings, search, charts and statistics.
          </p>
        </div>
        <span className="status-badge">
          {projectId ? `Project ${projectId.slice(0, 8)}` : 'No project'}
        </span>
      </div>
      <div className="analysis-sections">
        <Information projectId={projectId} />
        <Findings projectId={projectId} />
        <Search projectId={projectId} />
        <section className="analysis-panel">
          <h2>Charts</h2>
          <AnalysisChartPage />
        </section>
        <section className="analysis-panel">
          <h2>Statistic</h2>
          <StatisticsPage />
        </section>
      </div>
    </section>
  )
}
function Information({ projectId }: { projectId: string }) {
  const [project, setProject] = useState<ProjectSummary | undefined>()
  const [files, setFiles] = useState<LogFileSummary[]>([])
  const [total, setTotal] = useState<string>('-')
  const [period, setPeriod] = useState('-')
  useEffect(() => {
    if (!projectId) return
    void listProjects().then((r) =>
      setProject((r.results ?? []).find((p) => String(p.project_id) === projectId)),
    )
    void listLogFiles(projectId).then((r) => setFiles(r.results ?? []))
    void apiRequest<{ results?: Array<{ result_count?: number }> }>({
      method: 'POST',
      url: '/logdetail_dynamic/statistics/',
      data: { project_id: projectId, type: 0, N: 0 },
    }).then((r) => setTotal(String(r.results?.[0]?.result_count ?? 0)))
    void fetchPeriod(projectId, 'admin')
      .then((r) =>
        setPeriod(
          `${r.start_date ?? '-'} ${r.start_time ?? ''} ~ ${r.end_date ?? '-'} ${r.end_time ?? ''}`,
        ),
      )
      .catch(() => undefined)
  }, [projectId])
  const formats =
    Array.from(new Set(files.map((f) => f.file_format).filter(Boolean))).join(' / ') || '-'
  return (
    <div className="analysis-panel">
      <h2>Information</h2>
      <div className="info-grid">
        <b>Project Name</b>
        <span>{project?.project_name || '-'}</span>
        <b>Total Log Lines</b>
        <span>{Number(total).toLocaleString()} lines</span>
        <b>Logfile Name</b>
        <span>
          {files
            .map((f) => f.file_name)
            .filter(Boolean)
            .join(', ') || '-'}
        </span>
        <b>LogFormat</b>
        <span>{formats}</span>
        <b>Period (Date/Time)</b>
        <span>{period}</span>
      </div>
    </div>
  )
}
function Findings({ projectId }: { projectId: string }) {
  const [rows, setRows] = useState<Record<string, unknown>[]>([])
  const [status, setStatus] = useState('Load findings for this project.')
  const load = async () => {
    setStatus('Loading...')
    try {
      const result = await apiRequest<{ findingsResult?: Record<string, unknown>[] }>({
        method: 'POST',
        url: '/logdetail_dynamic/findings/',
        data: { project_id: projectId, filter: {} },
      })
      setRows(result.findingsResult ?? [])
      setStatus('')
    } catch {
      setStatus('Findings API unavailable.')
    }
  }
  return (
    <div className="analysis-panel">
      <h2>Findings</h2>
      <button onClick={() => void load()} disabled={!projectId}>
        Load findings
      </button>
      {status && <p role="status">{status}</p>}
      {rows.length > 0 && (
        <div style={{ overflow: 'auto' }}>
          <table>
            <thead>
              <tr>
                {Object.keys(rows[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, i) => (
                <tr key={i}>
                  {Object.keys(rows[0]).map((key) => (
                    <td key={key}>{String(row[key] ?? '')}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
function Search({ projectId }: { projectId: string }) {
  const [files, setFiles] = useState<import('@/features/init/service').LogFileSummary[]>([])
  const [selected, setSelected] = useState<string[]>([])
  const [period, setPeriod] = useState({ from: '', to: '' })
  // Keep the period returned for the project so Initialize can restore it
  // after the user edits the date/time controls.
  const [initialPeriod, setInitialPeriod] = useState({ from: '', to: '' })
  const [condition, setCondition] = useState('N')
  const [keyword, setKeyword] = useState('')
  const [exclude, setExclude] = useState(false)
  const [timeTaken, setTimeTaken] = useState(['', ''])
  useEffect(() => {
    if (!projectId) return
    void listLogFiles(projectId).then((r) => setFiles(r.results ?? []))
    void fetchPeriod(projectId, 'admin')
      .then((r) => {
        const next = {
          from: `${r.start_date ?? ''} ${r.start_time ?? ''}`,
          to: `${r.end_date ?? ''} ${r.end_time ?? ''}`,
        }
        setPeriod(next)
        setInitialPeriod(next)
      })
      .catch(() => undefined)
  }, [projectId])
  const instances = Array.from(
    new Set(files.map((f) => `${f.server_name ?? '-'}-${f.instance_name ?? '-'}`)),
  )
  // Match the original Analysis screen: all configured server/instances are
  // selected when the project is first loaded.
  useEffect(() => {
    setSelected(instances)
    // `instances` is derived from the just-loaded file list; only react when
    // that list changes so manual checkbox edits are preserved.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [files])
  const conditions = [
    ['N', 'None'],
    ['I', 'IP'],
    ['R', 'Request'],
    ['E', 'Referrer'],
    ['U', 'UserAgent'],
    ['S', 'Status'],
  ]
  const initialize = () => {
    setSelected(instances)
    setPeriod(initialPeriod)
    setCondition('N')
    setKeyword('')
    setExclude(false)
    setTimeTaken(['', ''])
  }
  const search = () => {
    const query = new URLSearchParams({
      project_id: projectId,
      conditionValue: condition,
      searchValue: keyword,
      excludeSearch: String(exclude),
      projectServers: selected.join(','),
      ttFromValue: timeTaken[0],
      ttToValue: timeTaken[1],
      dateFromValue: period.from.slice(0, 8),
      dateToValue: period.to.slice(0, 8),
      timeFromValue: period.from.slice(9),
      timeToValue: period.to.slice(9),
    })
    window.history.replaceState({}, '', `/analysis?${query.toString()}`)
    const detail = { ...Object.fromEntries(query), projectServers: selected }
    window.dispatchEvent(
      new CustomEvent('elao:analysis-search', { detail }),
    )
  }
  return (
    <div className="analysis-panel">
      <h2>Search</h2>
      <div className="search-form">
        <fieldset>
          <legend>Instances</legend>
          {instances.length === 0 && <span className="muted">No configured instances</span>}
          {instances.map((item) => (
            <label className="inline-check" key={item}>
              <input
                type="checkbox"
                checked={selected.includes(item)}
                onChange={(e) =>
                  setSelected(
                    e.target.checked ? [...selected, item] : selected.filter((x) => x !== item),
                  )
                }
              />
              {item}
            </label>
          ))}
        </fieldset>
        <fieldset>
          <legend>Date / Time</legend>
          <div className="datetime-row">
            <input
              type="date"
              title="Start date"
              value={
                period.from.slice(0, 8)
                  ? `${period.from.slice(0, 4)}-${period.from.slice(4, 6)}-${period.from.slice(6, 8)}`
                  : ''
              }
              onChange={(e) =>
                setPeriod((p) => ({
                  ...p,
                  from: e.target.value.replaceAll('-', '') + p.from.slice(8),
                }))
              }
            />
            <TimeSelect
              value={period.from.slice(9)}
              onChange={(v) => setPeriod((p) => ({ ...p, from: `${p.from.slice(0, 8)} ${v}` }))}
            />
            <span>~</span>
            <input
              type="date"
              title="End date"
              value={
                period.to.slice(0, 8)
                  ? `${period.to.slice(0, 4)}-${period.to.slice(4, 6)}-${period.to.slice(6, 8)}`
                  : ''
              }
              onChange={(e) =>
                setPeriod((p) => ({ ...p, to: e.target.value.replaceAll('-', '') + p.to.slice(8) }))
              }
            />
            <TimeSelect
              value={period.to.slice(9)}
              onChange={(v) => setPeriod((p) => ({ ...p, to: `${p.to.slice(0, 8)} ${v}` }))}
            />
          </div>
        </fieldset>
        <fieldset>
          <legend>Condition</legend>
          <div className="condition-row">
            <select value={condition} onChange={(e) => setCondition(e.target.value)}>
              {conditions.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
            <input
              placeholder="Enter your keyword"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
            />
            <label className="inline-check">
              <input
                type="checkbox"
                checked={exclude}
                onChange={(e) => setExclude(e.target.checked)}
              />{' '}
              Exclude
            </label>
          </div>
        </fieldset>
        <fieldset>
          <legend>TimeTaken</legend>
          <div className="condition-row">
            <input
              placeholder="ms"
              value={timeTaken[0]}
              onChange={(e) => setTimeTaken([e.target.value, timeTaken[1]])}
            />
            <span>~</span>
            <input
              placeholder="ms"
              value={timeTaken[1]}
              onChange={(e) => setTimeTaken([timeTaken[0], e.target.value])}
            />
          </div>
        </fieldset>
      </div>
      <p className="muted">Select instances and filters, then continue to raw log search.</p>
      <div className="search-actions">
        <button type="button" onClick={initialize}>
          Initialize
        </button>
        <button type="button" className="primary-action" onClick={search}>
          Search
        </button>
        <Link className="primary-link" to={`/lookup?project_id=${encodeURIComponent(projectId)}`}>
          Open Lookup search
        </Link>
      </div>
    </div>
  )
}
function TimeSelect({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  const raw = value.padEnd(6, '0')
  return (
    <div className="time-select">
      <select
        value={raw.slice(0, 2)}
        onChange={(e) => onChange(`${e.target.value}${raw.slice(2)}`)}
      >
        {Array.from({ length: 24 }, (_, i) => (
          <option key={i}>{String(i).padStart(2, '0')}</option>
        ))}
      </select>
      <select
        value={raw.slice(2, 4)}
        onChange={(e) => onChange(`${raw.slice(0, 2)}${e.target.value}${raw.slice(4)}`)}
      >
        {Array.from({ length: 60 }, (_, i) => (
          <option key={i}>{String(i).padStart(2, '0')}</option>
        ))}
      </select>
      <select
        value={raw.slice(4, 6)}
        onChange={(e) => onChange(`${raw.slice(0, 4)}${e.target.value}`)}
      >
        {Array.from({ length: 60 }, (_, i) => (
          <option key={i}>{String(i).padStart(2, '0')}</option>
        ))}
      </select>
    </div>
  )
}
