import { useEffect, useRef, useState, type FormEvent } from 'react'
import { createPortal } from 'react-dom'
import { createLogFormat, listLogFormatKinds, type LogFormatSummary } from './service'

export function AddLogFormatDialog({ creator, initialFormat, onClose, onSaved }: {
  creator: string; initialFormat?: { format_kind?: string; format_name?: string; format_strings?: string }
  onClose: () => void; onSaved: (format: LogFormatSummary) => void
}) {
  const dialog = useRef<HTMLDialogElement>(null)
  const savingRef = useRef(false)
  const [kinds, setKinds] = useState<string[]>([])
  const [kind, setKind] = useState(initialFormat?.format_kind ?? '')
  const [name, setName] = useState(initialFormat?.format_name ?? '')
  const [strings, setStrings] = useState(initialFormat?.format_strings ?? '')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [retry, setRetry] = useState(0)
  useEffect(() => {
    const element = dialog.current!
    element.showModal()
    return () => element.close()
  }, [])
  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')
    void listLogFormatKinds().then((result) => {
      if (!active) return
      setKinds(result.list_format_kind)
      if (!result.list_format_kind.length) setError('등록 가능한 포맷 종류가 없습니다.')
    }).catch(() => { if (active) setError('포맷 종류를 불러오지 못했습니다. 다시 시도해 주세요.') })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [retry])
  const save = async (event: FormEvent) => {
    event.preventDefault()
    if (savingRef.current || loading || !kind || !name.trim() || !strings.trim() || !creator) return
    savingRef.current = true
    setSaving(true)
    setError('')
    try {
      const result = await createLogFormat({ format_kind: kind, format_name: name.trim(), format_strings: strings.trim(), creator })
      onSaved(result)
    } catch { setError('로그 포맷을 저장하지 못했습니다. 입력값과 API 연결을 확인해 주세요.') }
    finally { savingRef.current = false; setSaving(false) }
  }
  return createPortal(
    <dialog ref={dialog} className="dense-card initialization-workspace log-format-dialog" aria-labelledby="add-log-format-title"
      onCancel={(event) => { event.preventDefault(); if (!savingRef.current) onClose() }}>
      <form onSubmit={(event) => void save(event)} aria-busy={saving}>
        <div className="log-format-dialog-heading">
          <h2 id="add-log-format-title">Add Log Format</h2>
          <button type="button" aria-label="Close log format dialog" disabled={saving} onClick={onClose}>×</button>
        </div>
        <p className="muted">로그 파일에 사용된 포맷을 등록하세요. 모든 항목은 필수입니다.</p>
        <div className="log-format-fields">
          <label>Format Kind<select required value={kind} disabled={loading || saving} onChange={(event) => setKind(event.target.value)}>
            <option value="">{loading ? 'Loading...' : 'Select format kind'}</option>
            {kinds.map((value) => <option key={value} value={value}>{value === 'jeus' ? 'jeus (>= ver7)' : value}</option>)}
          </select></label>
          <label>Format Name<input required maxLength={50} pattern="[^/]+" title="포맷 이름에는 /를 사용할 수 없습니다." placeholder="common, combined, main..." value={name} disabled={saving} onChange={(event) => setName(event.target.value)} /></label>
          <label>Format Strings<textarea required maxLength={500} rows={4} spellCheck={false} placeholder={'%h %l %u %t "%r" %>s %b'} value={strings} disabled={saving} onChange={(event) => setStrings(event.target.value)} /></label>
          <label>Creator<input readOnly value={creator} /></label>
        </div>
        {error && <p role="alert">{error}</p>}
        {!loading && !kinds.length && <button type="button" onClick={() => setRetry((value) => value + 1)}>Retry</button>}
        <div className="wizard-actions">
          <button type="button" disabled={saving} onClick={onClose}>Cancel</button>
          <button type="submit" disabled={loading || saving || !kind || !name.trim() || !strings.trim() || !creator}>{saving ? 'Saving...' : 'Save'}</button>
        </div>
      </form>
    </dialog>, document.body,
  )
}
