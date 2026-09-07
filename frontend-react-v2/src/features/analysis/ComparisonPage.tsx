import { useState } from 'react'
import ReactECharts from 'echarts-for-react'
import { fetchComparison, type ChartPayload } from './service'

export function ComparisonPage() {
  const [data, setData] = useState<ChartPayload | null>(null)
  const [status, setStatus] = useState('Ready')
  const load = async () => {
    setStatus('Loading...')
    try {
      setData(await fetchComparison({}))
      setStatus('')
    } catch {
      setStatus('Comparison API unavailable.')
    }
  }
  const values = (data?.resultXY ?? []).map((entry) => Number(entry.value ?? 0))
  return (
    <section className="dense-card">
      <h1>Comparison</h1>
      <button onClick={() => void load()}>Load comparison</button>
      {status && <p role="status">{status}</p>}
      <ReactECharts
        option={{
          animation: false,
          tooltip: {},
          xAxis: { type: 'category', data: data?.resultXY?.map((entry) => entry.name ?? '') ?? [] },
          yAxis: { type: 'value' },
          series: [{ type: 'bar', data: values }],
        }}
        style={{ height: 380 }}
        notMerge
        lazyUpdate
      />
    </section>
  )
}
