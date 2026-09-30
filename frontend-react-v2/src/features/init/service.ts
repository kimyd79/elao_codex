import { apiRequest } from '@/lib/api/client'
export type ProjectSummary = {
  project_id: number | string
  project_name: string
  project_description?: string
  creator?: string
  created?: string
}
export type LogFormatSummary = {
  format_id: number | string
  format_kind?: string
  format_name?: string
  format?: string
  format_strings?: string
}
export type LogFileSummary = {
  logfile_id: number | string
  file_name?: string
  file_size?: number
  file_format?: string
  server_name?: string
  instance_name?: string
  created?: string
}
export async function listProjects(creator?: string) {
  return apiRequest<{ results?: ProjectSummary[] }>({
    method: 'GET',
    url: '/logmaster/',
    params: creator ? { creator } : undefined,
  })
}
export async function listLogFormats(formatKind?: string) {
  return apiRequest<{ results?: LogFormatSummary[] }>({
    method: 'GET',
    url: '/logformat/',
    params: formatKind ? { format_kind: formatKind } : undefined,
  })
}
export async function listLogFiles(projectId: string) {
  return apiRequest<{ results?: LogFileSummary[] }>({
    method: 'GET',
    url: '/logfile/',
    params: { project: projectId },
  })
}
export function deleteLogFile(logfileId: string | number) {
  return apiRequest<void>({ method: 'DELETE', url: `/logfile/${encodeURIComponent(String(logfileId))}/` })
}
export function deleteProject(projectId: string | number) {
  return apiRequest<void>({ method: 'DELETE', url: `/logmaster/${encodeURIComponent(String(projectId))}/`, timeout: 120_000 })
}
export type FormatDetectionResult = {
  sample_count: number
  exact: boolean
  candidates: Array<{ format_id: string; format_kind: string; format_name: string; format_strings: string; valid_count: number; inferred?: boolean }>
}
export function detectLogFormat(file: File, signal?: AbortSignal) {
  const data = new FormData()
  data.append('file_object', file)
  return apiRequest<FormatDetectionResult>({ method: 'POST', url: '/logfile/detect_format/', data, signal, timeout: 15_000 })
}
export function listLogFormatKinds() {
  return apiRequest<{ list_format_kind: string[] }>({ method: 'GET', url: '/logformatstring/formatkind_list/' })
}
export function createLogFormat(data: { format_kind: string; format_name: string; format_strings: string; creator: string }) {
  return apiRequest<LogFormatSummary>({ method: 'POST', url: '/logformat/', data })
}
export async function createProject(data: {
  project_name: string
  project_description?: string
  creator: string
}) {
  return apiRequest<ProjectSummary>({ method: 'POST', url: '/logmaster/', data })
}
export async function createDynamicLogDetail(projectId: string) {
  return apiRequest<unknown>({
    method: 'POST',
    url: '/logmaster/create_dynamic_logdetail/',
    data: { project_id: projectId },
  })
}
export async function uploadLogFile(
  projectId: string,
  file: File,
  format: string,
  serverName: string,
  instanceName: string,
  onProgress?: (percent: number) => void,
  signal?: AbortSignal,
) {
  const [formatKind = '', formatName = '', ...formatParts] = format.split('/')
  const fileFormat = formatParts.join('/')
  if (!formatKind || !formatName || !fileFormat) throw new Error('Select a valid log format.')
  const data = new FormData()
  data.append('project', projectId)
  data.append('file_object', file)
  data.append('file_name', file.name)
  data.append('file_size', String(file.size))
  data.append('format_kind', formatKind)
  data.append('format_name', formatName)
  data.append('file_format', fileFormat)
  data.append('server_name', serverName)
  data.append('instance_name', instanceName)
  return apiRequest<{ logfile_id: string | number; file_name: string }>({
    method: 'POST',
    url: '/logfile/',
    data,
    signal,
    onUploadProgress: (event) => {
      if (event.total) onProgress?.(Math.round((event.loaded / event.total) * 100))
    },
  })
}

export type ParseResult = {
  status: string
  source_count: number
  parsed_count: number
  stored_count: number
  rejected_count: number
  files: Array<{
    logfile_id: string; file_name?: string; status: string
    source_count?: number; parsed_count: number; stored_count: number; rejected_count?: number
    failure_reasons?: Array<{ error_code: string; error_message: string; count: number }>
    failure_samples?: Array<{ line_number: number; error_code: string; error_message: string; raw_line_excerpt: string; truncated: boolean }>
  }>
}

export type AnalysisJob = {
  job_id: string
  status: string
  phase: string
  processed_units: number
  total_units: number
  progress_unit: string
}

export async function listAnalysisJobs(projectId: string, runId: string, signal: AbortSignal) {
  const jobs: AnalysisJob[] = []
  let page = 1
  for (;;) {
    const result = await apiRequest<{ results: AnalysisJob[]; next?: string | null }>({
      method: 'GET', url: '/loganalysisjob/',
      params: { project: projectId, run_id: runId, page }, signal, timeout: 5000,
    })
    jobs.push(...result.results)
    if (!result.next) return jobs
    page += 1
  }
}

export async function parseProjectFiles(projectId: string, logfileIds: string[], runId?: string) {
  if (!projectId || !logfileIds.length) throw new Error('Upload or select at least one log file.')
  const result = await apiRequest<ParseResult>({
    method: 'POST', url: '/logdetail_dynamic/',
    data: { project_id: projectId, logfile_id: logfileIds, diff_hour: 0, ...(runId ? { run_id: runId } : {}) },
    // This legacy endpoint responds only after parsing and COPY have finished.
    timeout: 0,
    validateStatus: (status) => status === 200 || status === 500,
  })
  if (result.status === 'FAILED' && result.files?.length) return result
  if (result.status !== 'COMPLETED' || result.rejected_count < 0 ||
      result.rejected_count * 100 >= result.source_count ||
      result.source_count !== result.stored_count + result.rejected_count ||
      !(result.stored_count > 0) || result.parsed_count !== result.stored_count ||
      !logfileIds.every((id) => result.files?.some((file) => file.logfile_id === id &&
        ['COMPLETED', 'ALREADY_COMPLETED'].includes(file.status) && file.parsed_count === file.stored_count))) {
    throw new Error(`Parsing incomplete: stored ${result.stored_count ?? 0}, rejected ${result.rejected_count ?? 0}. Check parsing results before continuing.`)
  }
  return result
}
