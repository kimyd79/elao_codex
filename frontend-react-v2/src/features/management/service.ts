import { apiRequest } from '@/lib/api/client'

export type ManagementKind = 'project' | 'logformat' | 'metrics'

const urls: Record<ManagementKind, string> = {
  project: '/logmaster/',
  logformat: '/logformat/',
  metrics: '/metrics/',
}

export function managementUrl(kind: ManagementKind, id?: string | number) {
  return id === undefined ? urls[kind] : `${urls[kind]}${encodeURIComponent(String(id))}/`
}

export async function createResource(kind: ManagementKind, data: Record<string, unknown>) {
  return apiRequest<Record<string, unknown>>({ method: 'POST', url: managementUrl(kind), data })
}

export async function updateResource(
  kind: ManagementKind,
  id: string | number,
  data: Record<string, unknown>,
) {
  return apiRequest<Record<string, unknown>>({
    method: 'PATCH',
    url: managementUrl(kind, id),
    data,
  })
}

export async function deleteResource(kind: ManagementKind, id: string | number) {
  return apiRequest<void>({ method: 'DELETE', url: managementUrl(kind, id) })
}
