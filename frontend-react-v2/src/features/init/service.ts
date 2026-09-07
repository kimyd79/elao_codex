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
  const [formatKind = '', formatName = '', fileFormat = ''] = format.split('/')
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
