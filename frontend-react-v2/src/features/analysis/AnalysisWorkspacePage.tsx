import { useEffect, useRef, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { AnalysisChartPage, StatisticsPage } from './AnalysisChartPage'
import { apiRequest } from '@/lib/api/client'
import {
  listLogFiles,
  listProjects,
  type LogFileSummary,
  type ProjectSummary,
} from '@/features/init/service'
import { fetchPeriod } from './service'
import { Findings } from './Findings'
import { clearPreparedAnalysis, takePreparedAnalysis, type PreparedAnalysis } from './prepareAnalysis'

export function AnalysisWorkspacePage() {
  const [params] = useSearchParams()
  const projectId = params.get('project_id') ?? ''
  const [prepared] = useState(() => takePreparedAnalysis(projectId))
  const initial = prepared?.projectId === projectId ? prepared : undefined
  useEffect(() => () => clearPreparedAnalysis(), [])
  return (
    <section className="dense-card analysis-workspace">
      <div className="analysis-heading">
        <div>
          <p className="auth-kicker" style={{ color: '#5269d4' }}>
            ANALYSIS WORKSPACE
          </p>
          <h1 className="analysis-title">Analysis</h1>
          <p className="muted">
            Explore project information, findings, search, charts and statistics.
          </p>
        </div>
        <span className="status-badge">
          {projectId ? `Project ${projectId.slice(0, 8)}` : 'No project'}
        </span>
      </div>
      <div className="analysis-sections">
        <Information projectId={projectId} initial={initial} />
        <Findings key={projectId} projectId={projectId} initial={initial} />
        <Search projectId={projectId} initial={initial} />
        <section className="analysis-panel">
          <h2>Charts</h2>
          <AnalysisChartPage initial={initial} />
        </section>
        <section className="analysis-panel">
          <h2>Statistic</h2>
          <StatisticsPage initial={initial} />
        </section>
      </div>
    </section>
  )
}
function Information({ projectId, initial }: { projectId: string; initial?: PreparedAnalysis }) {
  const [project, setProject] = useState<ProjectSummary | undefined>(initial?.project)
  const [files, setFiles] = useState<LogFileSummary[]>(initial?.files ?? [])
  const [total, setTotal] = useState<string>(initial ? String(initial.total) : '-')
  const [period, setPeriod] = useState('-')
  const formatDate = (value: unknown) => {
    const text = String(value ?? '').replace(/[^0-9]/g, '')
    return text.length === 8 ? `${text.slice(0, 4)}-${text.slice(4, 6)}-${text.slice(6, 8)}` : String(value ?? '-')
  }
  const formatTime = (value: unknown) => {
    const raw = String(value ?? '').replace(/[^0-9]/g, '')
    if (!raw) return '-'
    const text = raw.padStart(6, '0')
    return text.length === 6 ? `${text.slice(0, 2)}:${text.slice(2, 4)}:${text.slice(4, 6)}` : String(value ?? '-')
  }
  useEffect(() => {
    if (!projectId) return
    if (initial) {
      const r = initial.period
      setPeriod(`${formatDate(r.start_date)} ${formatTime(r.start_time)}  ~  ${formatDate(r.end_date)} ${formatTime(r.end_time)}`)
      return
    }
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
          `${formatDate(r.start_date)} ${formatTime(r.start_time)}  ~  ${formatDate(r.end_date)} ${formatTime(r.end_time)}`,
        ),
      )
      .catch(() => undefined)
  }, [projectId, initial])
  const formats =
    Array.from(new Set(files.map((f) => f.file_format).filter(Boolean))).join(', ') || '-'
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
export function Search({ projectId, targetPath = '/analysis', onSearch, isolated = false, eventName = 'elao:analysis-search', title = 'Search', initial }: { projectId: string; targetPath?: string; onSearch?: (query: Record<string, unknown>) => void; isolated?: boolean; eventName?: string; title?: string; initial?: PreparedAnalysis }) {
  const navigate = useNavigate()
  const urlParams = new URLSearchParams(window.location.search)
  const urlSearch = window.location.search
  const initialServers = urlParams.get('projectServers')?.split(',').filter(Boolean) ?? []
  const [files, setFiles] = useState<import('@/features/init/service').LogFileSummary[]>([])
  const [selected, setSelected] = useState<string[]>(initialServers)
  const [period, setPeriod] = useState({ from: urlParams.get('dateFromValue') && urlParams.get('timeFromValue') ? `${urlParams.get('dateFromValue')} ${urlParams.get('timeFromValue')}` : '', to: urlParams.get('dateToValue') && urlParams.get('timeToValue') ? `${urlParams.get('dateToValue')} ${urlParams.get('timeToValue')}` : '' })
  // Keep the period returned for the project so Initialize can restore it
  // after the user edits the date/time controls.
  const [initialPeriod, setInitialPeriod] = useState({ from: '', to: '' })
  const [condition, setCondition] = useState(urlParams.get('conditionValue') ?? 'N')
  const [keyword, setKeyword] = useState(urlParams.get('searchValue') ?? '')
  const [exclude, setExclude] = useState(urlParams.get('excludeSearch') === 'true')
  const [timeTaken, setTimeTaken] = useState([urlParams.get('ttFromValue') ?? '', urlParams.get('ttToValue') ?? ''])
  const [searchError, setSearchError] = useState('')
  const initialSearchDone = useRef(false)
  useEffect(() => {
    if (!projectId) return
    if (initial) {
      initialSearchDone.current = true
      setFiles(initial.files)
      const next = { from: `${initial.period.start_date ?? ''} ${initial.period.start_time ?? ''}`, to: `${initial.period.end_date ?? ''} ${initial.period.end_time ?? ''}` }
      setPeriod({
        from: urlParams.get('dateFromValue') && urlParams.get('timeFromValue') ? `${urlParams.get('dateFromValue')} ${urlParams.get('timeFromValue')}` : next.from,
        to: urlParams.get('dateToValue') && urlParams.get('timeToValue') ? `${urlParams.get('dateToValue')} ${urlParams.get('timeToValue')}` : next.to,
      })
      setInitialPeriod(next)
      return
    }
    initialSearchDone.current = false
    void listLogFiles(projectId).then((r) => setFiles(r.results ?? []))
    void fetchPeriod(projectId, 'admin')
      .then((r) => {
        const next = {
          from: `${r.start_date ?? ''} ${r.start_time ?? ''}`,
          to: `${r.end_date ?? ''} ${r.end_time ?? ''}`,
        }
        const from = urlParams.get('dateFromValue') && urlParams.get('timeFromValue') ? `${urlParams.get('dateFromValue')} ${urlParams.get('timeFromValue')}` : next.from
        const to = urlParams.get('dateToValue') && urlParams.get('timeToValue') ? `${urlParams.get('dateToValue')} ${urlParams.get('timeToValue')}` : next.to
        setPeriod({ from, to })
        setInitialPeriod(next)
      })
      .catch(() => undefined)
  // urlParams is derived from urlSearch; keeping the primitive dependency
  // avoids rerunning this effect on every render.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId, urlSearch, initial])
  useEffect(() => {
    // Step3 enters Analysis with the project's initial values. Dispatch the
    // same event as the Search button once those values are available so the
    // charts and statistics do not remain blank until a manual click.
    if (isolated || !projectId || !files.length || !period.from || initialSearchDone.current) return
    initialSearchDone.current = true
    // Defer one tick so the Charts and Statistics listeners are mounted too.
    const timer = window.setTimeout(() => search({
      instances: selected.length ? selected : instances,
      period,
    }), 0)
    return () => window.clearTimeout(timer)
    // The initial search intentionally waits for the fetched project values;
    // the button-driven search remains independent of this effect.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId, files, period, selected])
  const instances = Array.from(
    new Set(files.map((f) => `${f.server_name ?? '-'}-${f.instance_name ?? '-'}`)),
  )
  // Match the original Analysis screen: all configured server/instances are
  // selected when the project is first loaded.
  useEffect(() => {
    if (!initialServers.length) setSelected(instances)
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
    setSearchError('')
    setSelected(instances)
    setPeriod(initialPeriod)
    setCondition('N')
    setKeyword('')
    setExclude(false)
    setTimeTaken(['', ''])
  }
  const search = (initial?: { instances?: string[]; period?: { from: string; to: string } }) => {
    const bounds = timeTaken.map((value) => value.trim() === '' ? null : Number(value))
    if (bounds.some((value) => value !== null && (!Number.isFinite(value) || value < 0))) {
      setSearchError('TimeTaken은 0 이상의 숫자(ms)를 입력해 주세요.')
      return
    }
    if (bounds[0] !== null && bounds[1] !== null && bounds[0] > bounds[1]) {
      setSearchError('TimeTaken의 왼쪽 값은 오른쪽 값보다 클 수 없습니다. 조회 범위를 확인해 주세요.')
      return
    }
    setSearchError('')
    const searchInstances = initial?.instances ?? selected
    const searchPeriod = initial?.period ?? period
    const query = new URLSearchParams({
      project_id: projectId,
      conditionValue: condition,
      searchValue: keyword,
      excludeSearch: String(exclude),
      projectServers: searchInstances.join(','),
      ttFromValue: timeTaken[0].trim(),
      ttToValue: timeTaken[1].trim(),
      dateFromValue: searchPeriod.from.slice(0, 8),
      dateToValue: searchPeriod.to.slice(0, 8),
      timeFromValue: searchPeriod.from.slice(9),
      timeToValue: searchPeriod.to.slice(9),
    })
    if (!isolated) navigate(`${targetPath}?${query.toString()}`, { replace: true })
    const detail = { ...Object.fromEntries(query), projectServers: searchInstances }
    onSearch?.(detail)
    window.dispatchEvent(
      new CustomEvent(eventName, { detail }),
    )
  }
  return (
    <div className="analysis-panel">
      <h2>{title}</h2>
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
      {searchError && <p role="alert" className="statistic-detail-error">{searchError}</p>}
      <div className="search-actions">
        <button type="button" onClick={initialize}>
          Initialize
        </button>
        <button type="button" className="primary-action" onClick={() => search()}>
          Search
        </button>
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
