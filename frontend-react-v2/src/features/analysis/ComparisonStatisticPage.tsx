import { useSearchParams } from 'react-router-dom'
import { Search } from './AnalysisWorkspacePage'
import { StatisticsPage } from './AnalysisChartPage'

export function ComparisonStatisticPage() {
  const [params] = useSearchParams()
  const projectId = params.get('project_id') ?? ''
  return (
    <section className="dense-card analysis-workspace comparison-workspace comparison-statistic">
      <div className="analysis-heading"><h1 className="analysis-title">Comparison - Statistic</h1></div>
      {!projectId && <p role="status">Select a project in Initialization, then open Comparison-Statistic from Analysis.</p>}
      <div className="comparison-columns">
        {[1, 2].map((side) => (
          <section className="comparison-side" key={`${projectId}-${side}`} aria-label={`Statistics comparison ${side}`}>
            <section className="analysis-panel comparison-findings"><h2>{side === 1 ? 'Findings' : 'Findings2'}</h2></section>
            <Search projectId={projectId} isolated title={`Search-${side}`} eventName={`elao:comparison-statistic-${side}`} />
            <h2>Statistics</h2>
            <StatisticsPage manual eventName={`elao:comparison-statistic-${side}`} />
          </section>
        ))}
      </div>
    </section>
  )
}
