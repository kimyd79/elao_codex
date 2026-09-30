import { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '@/app/auth'
import { DenseTabs } from '@/components/tabs/DenseTabs'
import { AddLogFormatDialog } from './AddLogFormatDialog'
import { ParsingProgress } from './ParsingProgress'
import { ParseResultDialog } from './ParseResultDialog'
import { prepareAnalysis } from '@/features/analysis/prepareAnalysis'
import { FormatDetectionDialog, type Candidate as FormatCandidate } from './FormatDetectionDialog'
import {
  createDynamicLogDetail,
  createProject,
  listLogFormats,
  listLogFiles,
  deleteLogFile,
  deleteProject,
  detectLogFormat,
  type FormatDetectionResult,
  type LogFileSummary,
  listProjects,
  uploadLogFile,
  parseProjectFiles,
  type LogFormatSummary,
  type ProjectSummary,
  type ParseResult,
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
  const [showFormatDialog, setShowFormatDialog] = useState(false)
  const [files, setFiles] = useState<File[]>([])
  const [status, setStatus] = useState('')
  const [pending, setPending] = useState(false)
  const [parsing, setParsing] = useState(false)
  const [analysisRunId, setAnalysisRunId] = useState('')
  const [parseResult, setParseResult] = useState<ParseResult | null>(null)
  const [formatDetection, setFormatDetection] = useState<FormatDetectionResult | null>(null)
  const [inferredFormat, setInferredFormat] = useState<FormatCandidate | null>(null)
  const uploadedFiles = useRef(new Map<File, string>())
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
  const hasProjectDetails = Boolean(state.projectName.trim() && state.projectDescription.trim())
  const canNext =
    state.step !== 'step1' ||
    (state.projectMode === 'new' ? hasProjectDetails : Boolean(state.projectId))
  const move = (direction: -1 | 1) =>
    setState((s) => {
      const next = moveStep(s, direction)
      // The project-create confirmation belongs to Step1. Do not carry it
      // into the log-source setup screen.
      if (s.step === 'step1' && next.step === 'step2') setStatus('')
      setParams({ step: next.step })
      return next
    })
  const save = async () => {
    if (!hasProjectDetails) return false
    setPending(true)
    setStatus('Saving project...')
    try {
      const p = await createProject({
        project_name: state.projectName,
        project_description: state.projectDescription,
        creator: userName ?? 'fixture-user',
      })
      await createDynamicLogDetail(String(p.project_id))
      update({ projectId: String(p.project_id) })
      setStatus('Project and dynamic schema created.')
      return true
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'Project creation failed.')
      return false
    } finally {
      setPending(false)
    }
  }
  const next = async () => {
    if (pending || !canNext) return
    if (state.step === 'step3') {
      const runId = crypto.randomUUID()
      setAnalysisRunId(runId)
      setPending(true)
      setParsing(true)
      setStatus('Parsing log files and saving to DB. Please wait until processing finishes.')
      try {
        const registered = await listLogFiles(state.projectId)
        const result = await parseProjectFiles(state.projectId, (registered.results ?? []).map((file) => String(file.logfile_id)), runId)
        setStatus(`${result.stored_count.toLocaleString()} log lines stored.`)
        setParseResult(result)
      } catch (error) {
        setStatus(error instanceof Error ? error.message : 'Parsing failed. Stay on Step3 and retry.')
      } finally {
        setPending(false)
        setParsing(false)
      }
      return
    }
    if (state.step === 'step1' && state.projectMode === 'new' && !state.projectId) {
      if (!(await save())) return
    }
    if (state.step === 'step2') {
      if ((state.projectMode === 'new' || state.addLogFiles) && files.length) {
        if (!(await upload())) return
      }
      try {
        const registered = await listLogFiles(state.projectId)
        if (!registered.results?.length) { setStatus('Upload at least one log file before continuing.'); return }
        setSavedFiles(registered.results)
      } catch { setStatus('Could not confirm uploaded files. Please retry.'); return }
    }
    move(1)
  }
  const upload = async () => {
    if (!state.projectId || !state.logFormat || !state.serverName.trim() || !state.instanceName.trim() || files.length === 0) {
      setStatus('Select a project, server, instance, format, and at least one file.')
      return false
    }
    controller.current?.abort()
    controller.current = new AbortController()
    setPending(true)
    try {
      for (const file of files) {
        if (uploadedFiles.current.get(file) === state.projectId) continue
        const registered = await uploadLogFile(
          state.projectId,
          file,
          state.logFormat,
          state.serverName,
          state.instanceName,
          setProgress,
          controller.current.signal,
        )
        uploadedFiles.current.set(file, state.projectId)
        setSavedFiles((current) => [...current, registered])
      }
      setSavedFiles((await listLogFiles(state.projectId)).results ?? [])
      setStatus(`${files.length} file(s) uploaded. Start Analysis in Step3 to parse and save logs.`)
      return true
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'File upload failed.')
      return false
    } finally {
      setPending(false)
    }
  }
  const removeSavedFile = async (file: LogFileSummary) => {
    if (!window.confirm(`Delete registered log file "${file.file_name || file.logfile_id}"?`)) return
    setPending(true)
    setStatus('Deleting log file and related parsed data...')
    try {
      await deleteLogFile(file.logfile_id)
      setSavedFiles((current) => current.filter((item) => item.logfile_id !== file.logfile_id))
      // A file uploaded during this wizard is also kept in the local
      // selection. Remove it there too, otherwise Step3 renders it as a new
      // file even after its registered record was deleted.
      setFiles((current) => current.filter((item) => item.name !== file.file_name))
      for (const selected of uploadedFiles.current.keys()) {
        if (selected.name === file.file_name) uploadedFiles.current.delete(selected)
      }
      setStatus('Log file deleted.')
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'Log file deletion failed.')
    } finally {
      setPending(false)
    }
  }
  const removeProject = async (project: ProjectSummary) => {
    if (!window.confirm(`Delete project "${project.project_name}" and all related log data?`)) return
    setPending(true)
    setStatus('Deleting project and related log data...')
    try {
      await deleteProject(project.project_id)
      setProjects((current) => current.filter((item) => item.project_id !== project.project_id))
      if (String(project.project_id) === state.projectId) {
        update({ projectId: '', projectName: '', projectDescription: '', addLogFiles: false })
        setSavedFiles([])
        setFiles([])
      }
      setStatus('Project deleted.')
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'Project deletion failed.')
    } finally {
      setPending(false)
    }
  }
  const detectSelectedFormat = async (selectedFiles: File[]) => {
    if (!selectedFiles[0]) return
    try {
      setFormatDetection(await detectLogFormat(selectedFiles[0]))
    } catch {
      setStatus('Could not detect a log format from the selected file.')
    }
  }
  const currentProject = useMemo(
    () => projects.find((p) => String(p.project_id) === state.projectId),
    [projects, state.projectId],
  )
  return (
    <>
    <section className="dense-card initialization-workspace">
      <div className="initialization-heading">
        <div>
          <p className="auth-kicker" style={{ color: '#5269d4' }}>
            WORKSPACE SETUP
          </p>
          <h1 className="initialization-title">Initialization</h1>
          <p className="muted">Set initial information for log analysis</p>
        </div>
        <span className="status-badge">
          {state.step === 'current' ? 'Review' : `Step ${index}`}
        </span>
      </div>
      <DenseTabs tabs={tabs} activeKey={state.step} readOnly />
      {showFormatDialog && <AddLogFormatDialog creator={userName ?? ''} initialFormat={inferredFormat ?? undefined} onClose={() => { setShowFormatDialog(false); setInferredFormat(null) }} onSaved={(format) => {
        setFormats((current) => [...current.filter((item) => item.format_id !== format.format_id), format])
        update({ logFormat: `${format.format_kind}/${format.format_name}/${format.format_strings ?? format.format ?? ''}` })
        setShowFormatDialog(false)
        setInferredFormat(null)
        setStatus('Log format saved and selected.')
      }} />}
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
                  <span>Actions</span>
                </div>
                {projects.length === 0 && (
                  <div className="project-empty">No existing projects found.</div>
                )}
                {projects.map((p) => (
                  <div className="project-row-wrap" key={p.project_id}>
                    <button
                      type="button"
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
                    <button type="button" className="danger-action project-delete-action" disabled={pending} onClick={() => void removeProject(p)}>
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}
            <label>
              Project Name
              <input
                value={state.projectName}
                readOnly={state.projectMode === 'existing'}
                onChange={(e) => update({ projectName: e.target.value })}
              />
            </label>
            <label>
              Project Description
              <textarea
                rows={3}
                value={state.projectDescription}
                readOnly={state.projectMode === 'existing'}
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
              <button disabled={pending || !hasProjectDetails} onClick={() => void save()}>
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
                    <button type="button" className="danger-action" disabled={pending} onClick={() => void removeSavedFile(file)}>
                      Delete
                    </button>
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
              <div className="wide">
                <label htmlFor="init-file-format">File Format</label>
                <div className="log-format-selector">
                <select
                  id="init-file-format"
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
                <button type="button" disabled={pending} onClick={() => { setInferredFormat(null); setShowFormatDialog(true) }}>+ Add Format</button>
                </div>
              </div>
            )}
            {(state.projectMode === 'new' || state.addLogFiles) && (
              <label className="wide">
                Files
                <input
                  type="file"
                  multiple
                  disabled={pending}
                  onChange={(e) => {
                    const selected = Array.from(e.target.files ?? [])
                    setFiles(selected)
                    void detectSelectedFormat(selected)
                  }}
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
              <button disabled={pending || files.length === 0} onClick={() => void upload()}>
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
              <span>{savedFiles.length + files.filter((file) => !savedFiles.some((saved) => saved.file_name === file.name)).length || 'Existing files'}</span>
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
              {files.filter((file) => !savedFiles.some((saved) => saved.file_name === file.name)).map((file) => (
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
        <div className={`status-message${parsing ? ' parsing-status' : ''}`} aria-busy={parsing}>
          <span role="status">{status}</span>
          {parsing && <ParsingProgress projectId={state.projectId} runId={analysisRunId} />}
        </div>
      )}
      <div className="wizard-actions">
        <button disabled={index === 0 || pending} onClick={() => move(-1)}>
          Prev
        </button>
        <button
          disabled={pending || (!canNext && state.step !== 'step3')}
          onClick={() => void next()}
        >
          {state.step === 'step3' ? 'Start Analysis' : 'Next'}
        </button>
        {pending && !parsing && <button onClick={() => controller.current?.abort()}>Cancel</button>}
      </div>
    </section>
    {parseResult && <ParseResultDialog result={parseResult} onClose={() => setParseResult(null)} onContinue={async (onProgress) => {
      await prepareAnalysis(state.projectId, onProgress)
      navigate(`/analysis?project_id=${encodeURIComponent(state.projectId)}`)
    }} />}
    <FormatDetectionDialog
      open={formatDetection !== null}
      sampleCount={formatDetection?.sample_count ?? 0}
      exact={formatDetection?.exact ?? false}
      candidates={formatDetection?.candidates ?? []}
      onClose={() => setFormatDetection(null)}
      onSelect={(candidate) => {
        setFormatDetection(null)
        if (candidate.inferred) {
          setInferredFormat(candidate)
          setShowFormatDialog(true)
          setStatus('Review the inferred format and save it to register.')
          return
        }
        update({ logFormat: `${candidate.format_kind}/${candidate.format_name}/${candidate.format_strings}` })
        setStatus('Registered log format selected.')
      }}
    />
    </>
  )
}
