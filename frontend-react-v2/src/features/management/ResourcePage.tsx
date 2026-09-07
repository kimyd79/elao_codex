import { useCallback, useEffect, useState, type FormEvent } from 'react'
import { apiRequest } from '@/lib/api/client'
import { createResource, type ManagementKind } from './service'

type Resource = Record<string, unknown> & {
  id?: string | number
  project_id?: string | number
  format_id?: string | number
  metric_id?: string | number
}
const configs: Record<ManagementKind, { title: string; url: string; fields: string[] }> = {
  project: {
    title: 'Projects',
    url: '/logmaster/',
    fields: ['project_name', 'project_description', 'creator'],
  },
  logformat: {
    title: 'Log Formats',
    url: '/logformat/',
    fields: ['format_kind', 'format_name', 'format_strings', 'creator'],
  },
  metrics: {
    title: 'Metrics',
    url: '/metrics/',
    fields: [
      'metric_kind',
      'metric_type',
      'metric_definition',
      'metric_filter',
      'metric_unit',
      'metric_static',
      'creator',
    ],
  },
}

export function ResourcePage({ kind }: { kind: ManagementKind }) {
  const config = configs[kind]
  const [items, setItems] = useState<Resource[]>([])
  const [status, setStatus] = useState('Loading...')
  const [draft, setDraft] = useState<Record<string, string>>({})
  const load = useCallback(async () => {
    setStatus('Loading...')
    try {
      const data = await apiRequest<{ results?: Resource[] } | Resource[]>({
        method: 'GET',
        url: config.url,
      })
      setItems(Array.isArray(data) ? data : (data.results ?? []))
      setStatus('')
    } catch {
      setStatus('API 조회에 실패했습니다.')
    }
  }, [config.url])
  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setStatus('Saving...')
    try {
      await createResource(kind, draft)
      setDraft({})
      await load()
    } catch {
      setStatus('Save failed.')
    }
  }
  useEffect(() => {
    void load()
  }, [load])
  const columns = items.length ? Object.keys(items[0]).slice(0, 6) : []
  return (
    <section className="dense-card">
      <h1>{config.title}</h1>
      <button onClick={() => void load()}>Refresh</button>
      <form onSubmit={submit} style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 10 }}>
        {config.fields.map((field) => (
          <input
            key={field}
            aria-label={field}
            placeholder={field}
            value={draft[field] ?? ''}
            onChange={(event) =>
              setDraft((current) => ({ ...current, [field]: event.target.value }))
            }
          />
        ))}
        <button type="submit">Create</button>
      </form>
      {status && <p role="status">{status}</p>}
      {items.length > 0 && (
        <div style={{ overflow: 'auto', marginTop: 12 }}>
          <table>
            <thead>
              <tr>
                {columns.map((column) => (
                  <th key={column} style={{ textAlign: 'left', padding: 6 }}>
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {items.map((item, index) => (
                <tr
                  key={String(
                    item.id ?? item.project_id ?? item.format_id ?? item.metric_id ?? index,
                  )}
                >
                  {columns.map((column) => (
                    <td key={column} style={{ padding: 6, borderTop: '1px solid #eee' }}>
                      {String(item[column] ?? '')}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {!status && items.length === 0 && <p className="muted">No data</p>}
    </section>
  )
}
