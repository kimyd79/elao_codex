import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AgGridReact } from 'ag-grid-react'
import { AllCommunityModule, ModuleRegistry, type ColDef } from 'ag-grid-community'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-quartz.css'
import { fetchLogs, type LogRow } from './service'

ModuleRegistry.registerModules([AllCommunityModule])

export function LookupPageV2() {
  const navigate = useNavigate()
  const [rows, setRows] = useState<LogRow[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(false)
  const [nextCursor, setNextCursor] = useState<string | null>(null)
  const [selected, setSelected] = useState<LogRow | null>(null)
  const controller = useRef<AbortController | null>(null)
  const columns = useMemo<ColDef<LogRow>[]>(
    () => [
      { field: 'id', headerName: 'ID', width: 100 },
      { field: 'line_no', headerName: 'Line', width: 100 },
      { field: 'raw_log', headerName: 'Raw Log', flex: 1, minWidth: 360 },
    ],
    [],
  )
  const load = useCallback(
    async (cursor: string | null = null) => {
      controller.current?.abort()
      controller.current = new AbortController()
      setLoading(true)
      try {
        const page = await fetchLogs({ cursor, limit: 100, search }, controller.current.signal)
        const items = page.items ?? page.results ?? []
        setRows((current) => (cursor ? [...current, ...items] : items))
        setNextCursor(page.next_cursor ?? page.next ?? null)
      } finally {
        setLoading(false)
      }
    },
    [search],
  )
  useEffect(() => {
    void load()
  }, [load])
  const onRowClicked = (event: { data?: LogRow }) => {
    if (!event.data) return
    setSelected(event.data)
    if (event.data.project_id)
      navigate(
        `/detail?project_id=${encodeURIComponent(String(event.data.project_id))}&logfile_id=${encodeURIComponent(String(event.data.logfile_id ?? ''))}&line_no=${encodeURIComponent(String(event.data.line_no ?? ''))}`,
      )
  }
  return (
    <section className="dense-card">
      <h1>Lookup</h1>
      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        <input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="검색어"
        />
        <button onClick={() => void load()}>Search</button>
        {nextCursor && <button onClick={() => void load(nextCursor)}>Load next</button>}
      </div>
      <div className="ag-theme-quartz" style={{ height: 480, width: '100%' }}>
        <AgGridReact
          rowData={rows}
          columnDefs={columns}
          getRowId={(params) =>
            String(params.data.id ?? `${params.data.logfile_id}-${params.data.line_no}`)
          }
          onRowClicked={onRowClicked}
          loading={loading}
        />
      </div>
      {selected && (
        <p role="status">Selected line: {String(selected.line_no ?? selected.id ?? '')}</p>
      )}
    </section>
  )
}
