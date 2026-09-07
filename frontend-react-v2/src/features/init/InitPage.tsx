import { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '@/app/auth'
import { DenseTabs } from '@/components/tabs/DenseTabs'
import {
  createDynamicLogDetail,
  createProject,
  listLogFormats,
  listLogFiles,
  type LogFileSummary,
  listProjects,
  uploadLogFile,
  type LogFormatSummary,
  type ProjectSummary,
} from './service'
import { initialInitState, initSteps, moveStep, stepIndex, type InitState } from './state'

const tabs = initSteps.map((key) => ({
  key,
  label: key === 'current' ? 'Current Info' : key[0].toUpperCase() + key.slice(1),
  to: `/initialization?step=${key}`,
}))
export function InitPage() {
  const { userName } = useAuth()
  const navigate = useNavigate()
  const [params, setParams] = useSearchParams()
  const requested = params.get('step') as InitState['step'] | null
  const [state, setState] = useState<InitState>({
    ...initialInitState,
    step: requested && initSteps.includes(requested) ? requested : 'current',
  })
  const [projects, setProjects] = useState<ProjectSummary[]>([])
  const [savedFiles, setSavedFiles] = useState<LogFileSummary[]>([])
  const [formats, setFormats] = useState<LogFormatSummary[]>([])
  const [files, setFiles] = useState<File[]>([])
  const [status, setStatus] = useState('')
  const [pending, setPending] = useState(false)
  const [progress, setProgress] = useState(0)
  const controller = useRef<AbortController | null>(null)
  useEffect(() => {
    if (requested && initSteps.includes(requested) && requested !== state.step)
      setState((s) => ({ ...s, step: requested }))
  }, [requested, state.step])
  useEffect(() => {
    void listProjects()
      .then((r) => setProjects(r.results ?? []))
      .catch(() => undefined)
    void listLogFormats()
      .then((r) => setFormats(r.results ?? []))
      .catch(() => undefined)
  }, [])
  useEffect(() => {
    if (!state.projectId) {
      setSavedFiles([])
      return
    }
    void listLogFiles(state.projectId)
      .then((r) => {
        const rows = r.results ?? []
        setSavedFiles(rows)
        if (state.projectMode === 'existing' && rows[0])
          update({
            serverName: rows[0].server_name ?? '',
            instanceName: rows[0].instance_name ?? '',
            logFormat: rows[0].file_format ?? '',
          })
      })
      .catch(() => setSavedFiles([]))
  }, [state.projectId, state.projectMode])
  const update = (patch: Partial<InitState>) => setState((s) => ({ ...s, ...patch }))
  const index = stepIndex(state.step)
  const canNext =
    state.step !== 'step1' ||
    (state.projectMode === 'new' ? Boolean(state.projectId) : Boolean(state.projectId))
  const move = (direction: -1 | 1) =>
    setState((s) => {
      const next = moveStep(s, direction)
      setParams({ step: next.step })
      return next
    })
  const save = async () => {
    setPending(true)
    setStatus('Saving project...')
    try {
      const p = await createProject({
        project_name: state.projectName,
        project_description: state.projectDescription,
        creator: userName ?? 'fixture-user',
      })
      update({ projectId: String(p.project_id) })
      await createDynamicLogDetail(String(p.project_id))
      setStatus('Project and dynamic schema created.')
    } catch {
      setStatus('Project creation failed.')
    } finally {
      setPending(false)
    }
  }
  const upload = async () => {
    if (!state.projectId || !state.logFormat || files.length === 0) {
      setStatus('Select a project, format, and at least one file.')
      return
    }
    controller.current?.abort()
    controller.current = new AbortController()
    setPending(true)
    try {
      for (const file of files)
        await uploadLogFile(
          state.projectId,
          file,
          state.logFormat,
          state.serverName,
          state.instanceName,
          setProgress,
          controller.current.signal,
        )
      setStatus(`${files.length} file(s) uploaded.`)
    } catch {
      setStatus('File upload failed.')
    } finally {
      setPending(false)
    }
  }
  const currentProject = useMemo(
    () => projects.find((p) => String(p.project_id) === state.projectId),
    [projects, state.projectId],
  )
  return (
    <section className="dense-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
        <div>
          <p className="auth-kicker" style={{ color: '#5269d4' }}>
            WORKSPACE SETUP
          </p>
          <h1>Initialization</h1>
          <p className="muted">Set initial information for log analysis</p>
        </div>
        <span className="status-badge">
          {state.step === 'current' ? 'Review' : `Step ${index}`}
        </span>
      </div>
      <DenseTabs tabs={tabs} />
      <div role="tabpanel" style={{ minHeight: 260 }}>
        {state.step === 'current' && (
          <div>
            <h2>Current Info</h2>
            <p className="muted">
              Review the selected project and registered files before analysis.
            </p>
            {currentProject ? (
              <div className="info-grid">
                <b>Project</b>
                <span>{currentProject.project_name}</span>
                <b>Description</b>
                <span>{currentProject.project_description || '-'}</span>
                <b>Project ID</b>
                <span>{state.projectId}</span>
              </div>
            ) : (
              <p className="empty-state">No project selected. Start with Step1.</p>
            )}
          </div>
        )}
        {state.step === 'step1' && (
          <div className="form-grid project-form">
            <h2>Project</h2>
            <div className="segmented">
              <button
                className={state.projectMode === 'new' ? 'selected' : ''}
                onClick={() =>
                  update({
                    projectMode: 'new',
                    projectId: '',
                    projectName: '',
                    projectDescription: '',
                    addLogFiles: false,
                  })
                }
              >
                New
              </button>
              <button
                className={state.projectMode === 'existing' ? 'selected' : ''}
                onClick={() =>
                  update({
                    projectMode: 'existing',
                    projectId: '',
                    projectName: '',
                    projectDescription: '',
                    addLogFiles: false,
                  })
                }
              >
                Exist
              </button>
            </div>
            {state.projectMode === 'existing' && (
              <div className="project-table wide">
                <div className="project-table-head">
                  <span>Project Name</span>
                  <span>Project Description</span>
                  <span>Creator</span>
                  <span>Created Date</span>
                </div>
                {projects.length === 0 && (
                  <div className="project-empty">No existing projects found.</div>
                )}
                {projects.map((p) => (
                  <button
                    type="button"
                    key={p.project_id}
                    className={
                      String(p.project_id) === state.projectId
                        ? 'project-row selected'
                        : 'project-row'
                    }
                    onClick={() =>
                      update({
                        projectId: String(p.project_id),
                        projectName: p.project_name,
                        projectDescription: p.project_description ?? '',
                      })
                    }
                  >
                    <span>{p.project_name}</span>
                    <span>{p.project_description || '-'}</span>
                    <span>{p.creator || '-'}</span>
                    <span>{p.created ? new Date(p.created).toLocaleString() : '-'}</span>
                  </button>
                ))}
              </div>
            )}
            <label>
              Project Name
              <input
                value={state.projectName}
                onChange={(e) => update({ projectName: e.target.value })}
              />
            </label>
            <label>
              Project Description
              <textarea
                rows={3}
                value={state.projectDescription}
                onChange={(e) => update({ projectDescription: e.target.value })}
              />
            </label>
            {state.projectMode === 'existing' && (
              <label className="check">
                <input
                  type="checkbox"
                  checked={state.addLogFiles}
                  onChange={(e) => update({ addLogFiles: e.target.checked })}
                />{' '}
                Add Log Files
              </label>
            )}
            {state.projectMode === 'new' && (
              <button disabled={pending || !state.projectName.trim()} onClick={() => void save()}>
                Create project
              </button>
            )}
          </div>
        )}
        {state.step === 'step2' && (
          <div className="form-grid">
            <h2>Log source</h2>
            <div className="info-grid wide">
              <b>Project</b>
              <span>{state.projectName || '-'}</span>
              <b>Description</b>
              <span>{state.projectDescription || '-'}</span>
            </div>
            {state.projectMode === 'existing' && (
              <div className="saved-files wide">
                <strong>Saved log files</strong>
                {savedFiles.length === 0 && <p className="muted">No saved log files.</p>}
                {savedFiles.map((file) => (
                  <div className="saved-file" key={file.logfile_id}>
                    <span>{file.file_name || '-'}</span>
                    <span>{file.file_format || '-'}</span>
                    <span>
                      {file.server_name || '-'} / {file.instance_name || '-'}
                    </span>
                    <span>{file.file_size ? `${file.file_size.toLocaleString()} bytes` : '-'}</span>
                  </div>
                ))}
              </div>
            )}
            {state.projectMode === 'existing' && (
              <label className="check wide">
                <input
                  type="checkbox"
                  checked={state.addLogFiles}
                  onChange={(e) => update({ addLogFiles: e.target.checked })}
                />{' '}
                Add Log Files to this project
              </label>
            )}
            {(state.projectMode === 'new' || state.addLogFiles) && (
              <>
                <label>
                  Server Name
                  <input
                    value={state.serverName}
                    onChange={(e) => update({ serverName: e.target.value })}
                    placeholder="server-01"
                  />
                </label>
                <label>
                  Instance Name
                  <input
                    value={state.instanceName}
                    onChange={(e) => update({ instanceName: e.target.value })}
                    placeholder="instance-01"
                  />
                </label>
              </>
            )}
            {(state.projectMode === 'new' || state.addLogFiles) && (
              <label className="wide">
                File Format
                <select
                  value={state.logFormat}
                  onChange={(e) => update({ logFormat: e.target.value })}
                >
                  <option value="">Select format</option>
                  {formats.map((f) => (
                    <option
                      key={f.format_id}
                      value={`${f.format_kind ?? ''}/${f.format_name ?? ''}/${f.format_strings ?? f.format ?? ''}`}
                    >
                      {`${f.format_kind ?? '-'} / ${f.format_name ?? '-'} / ${f.format_strings ?? f.format ?? '-'}`}
                    </option>
                  ))}
                </select>
              </label>
            )}
            {(state.projectMode === 'new' || state.addLogFiles) && (
              <label className="wide">
                Files
                <input
                  type="file"
                  multiple
                  disabled={pending}
                  onChange={(e) => setFiles(Array.from(e.target.files ?? []))}
                />
              </label>
            )}
            {(state.projectMode === 'new' || state.addLogFiles) && files.length > 0 && (
              <div className="file-chips wide">
                {files.map((f) => (
                  <span key={f.name}>
                    {f.name} · {(f.size / 1024).toFixed(1)} KB
                  </span>
                ))}
              </div>
            )}
            <label>
              Data Range
              <select
                value={state.range}
                onChange={(e) => update({ range: e.target.value as InitState['range'] })}
              >
                <option value="all">ALL</option>
                <option value="select" disabled>
                  Select Range
                </option>
              </select>
            </label>
            {(state.projectMode === 'new' || state.addLogFiles) && (
              <button disabled={pending} onClick={() => void upload()}>
                Upload files
              </button>
            )}
            {pending && <progress className="wide" value={progress} max={100} />}
          </div>
        )}
        {state.step === 'step3' && (
          <div>
            <h2>Review & Analyze</h2>
            <div className="info-grid">
              <b>Project</b>
              <span>{state.projectName || '-'}</span>
              <b>Server</b>
              <span>{state.serverName || '-'}</span>
              <b>Instance</b>
              <span>{state.instanceName || '-'}</span>
              <b>Format</b>
              <span>{state.logFormat || '-'}</span>
              <b>Files</b>
              <span>{files.length || 'Existing files'}</span>
              <b>Range</b>
              <span>{state.range.toUpperCase()}</span>
            </div>
            <div className="saved-files review-files">
              <strong>Files to analyze</strong>
              {savedFiles.map((file) => (
                <div className="saved-file" key={`saved-${file.logfile_id}`}>
                  <span>{file.file_name || '-'}</span>
                  <span>{file.file_format || '-'}</span>
                  <span>
                    {file.server_name || '-'} / {file.instance_name || '-'}
                  </span>
                  <span>{file.file_size ? `${file.file_size.toLocaleString()} bytes` : '-'}</span>
                </div>
              ))}
              {files.map((file) => (
                <div className="saved-file" key={`new-${file.name}`}>
                  <span>{file.name}</span>
                  <span>{state.logFormat || '-'}</span>
                  <span>
                    {state.serverName || '-'} / {state.instanceName || '-'}
                  </span>
                  <span>{file.size.toLocaleString()} bytes</span>
                </div>
              ))}
              {savedFiles.length === 0 && files.length === 0 && (
                <p className="muted">No files selected.</p>
              )}
            </div>
          </div>
        )}
      </div>
      {status && (
        <p role="status" className="status-message">
          {status}
        </p>
      )}
      <div className="wizard-actions">
        <button disabled={index === 0 || pending} onClick={() => move(-1)}>
          Prev
        </button>
        <button
          disabled={pending || (!canNext && state.step !== 'step3')}
          onClick={() =>
            state.step === 'step3'
              ? navigate(`/analysis?project_id=${encodeURIComponent(state.projectId)}`)
              : move(1)
          }
        >
          {state.step === 'step3' ? 'Start Analysis' : 'Next'}
        </button>
        {pending && <button onClick={() => controller.current?.abort()}>Cancel</button>}
      </div>
    </section>
  )
}
