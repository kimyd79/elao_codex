import { useSearchParams } from 'react-router-dom'
import { Search } from './AnalysisWorkspacePage'
import { AnalysisChartPage } from './AnalysisChartPage'

export function ComparisonPage() {
  const [params] = useSearchParams()
  const projectId = params.get('project_id') ?? ''
  return (
    <section className="dense-card analysis-workspace comparison-workspace">
      <div className="analysis-heading"><h1 className="analysis-title">Comparison - Chart</h1></div>
      {!projectId && <p role="status">Select a project in Initialization, then open Comparison-Chart from Analysis.</p>}
      <div className="comparison-columns">
        {[1, 2].map((side) => (
          <section className="comparison-side" key={`${projectId}-${side}`} aria-label={`Comparison ${side}`}>
            <section className="analysis-panel comparison-findings"><h2>{side === 1 ? 'Findings' : 'Findings2'}</h2></section>
            <Search projectId={projectId} isolated title={`Search-${side}`} eventName={`elao:comparison-${side}`} />
            <h2>Charts</h2>
            <AnalysisChartPage eventName={`elao:comparison-${side}`} />
          </section>
        ))}
      </div>
    </section>
  )
}
