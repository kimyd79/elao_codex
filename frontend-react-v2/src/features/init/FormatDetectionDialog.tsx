export type Candidate = { format_id?: string; format_kind: string; format_name: string; format_strings: string; valid_count: number; inferred?: boolean }

export function FormatDetectionDialog({
  open, sampleCount, exact, candidates, onClose, onSelect,
}: { open: boolean; sampleCount: number; exact: boolean; candidates: Candidate[]; onClose: () => void; onSelect: (candidate: Candidate) => void }) {
  if (!open) return null
  return (
    <div className="format-detection-backdrop" role="presentation" onClick={onClose}>
      <section className="format-detection-dialog" role="dialog" aria-modal="true" aria-labelledby="format-detection-title" onClick={(e) => e.stopPropagation()}>
        <h3 id="format-detection-title">Detected access-log format</h3>
        <p className="muted">Checked {sampleCount} log lines from the selected file.</p>
        {candidates.length === 0 ? <p>No registered format matched this sample.</p> : (
          <>
            <p>{exact ? 'One format matched exactly:' : 'The following formats are the closest matches:'}</p>
            <div className="format-detection-list">
              {candidates.map((candidate) => (
                <button type="button" className="format-detection-item" key={`${candidate.format_kind}/${candidate.format_name}`} onClick={() => onSelect(candidate)}>
                  <strong>{candidate.format_kind} / {candidate.format_name}{candidate.inferred ? ' · inferred from sample' : ' · registered'}</strong>
                  <code>{candidate.format_strings}</code>
                  <span>{candidate.valid_count} matching lines</span>
                </button>
              ))}
            </div>
          </>
        )}
        <button type="button" className="format-detection-close" onClick={onClose}>Close</button>
      </section>
    </div>
  )
}
