import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { createRequire } from 'node:module'
import { chromium } from '@playwright/test'

const require = createRequire(import.meta.url)
const source = await readFile(new URL('../src/features/analysis/XViewPage.tsx', import.meta.url), 'utf8')
assert.match(source, /progressive: 0/)
const browser = await chromium.launch({ headless: true })
try {
  const page = await browser.newPage()
  await page.setContent('<div id="chart" style="width:900px;height:500px"></div>')
  await page.addScriptTag({ path: require.resolve('echarts/dist/echarts.js') })
  const results = await page.evaluate(async () => {
    const results = []
    for (const progressive of [5000, 0]) {
      const chart = window.echarts.init(document.getElementById('chart'))
      chart.setOption({
        animation: false,
        brush: { seriesIndex: [], xAxisIndex: 0, yAxisIndex: 0 },
        xAxis: { type: 'value' }, yAxis: { type: 'value' },
        series: [{ type: 'scatter', large: true, largeThreshold: 2000,
          progressive, progressiveThreshold: 8000,
          data: Array.from({ length: 12345 }, (_, i) => [i, i % 100]),
        }],
      })
      await new Promise((resolve) => setTimeout(resolve, 600))
      const count = () => chart.getZr().storage.getDisplayList(true)
        .reduce((total, element) => total + (element.shape?.points?.length / 2 || 0), 0)
      const before = count()
      const selections = []
      for (let i = 0; i < 3; i++) {
        chart.dispatchAction({ type: 'brush', areas: [{ brushType: 'rect',
          xAxisIndex: 0, yAxisIndex: 0, coordRange: [[100 + i, 200], [0, 50]],
        }] })
        await new Promise((resolve) => setTimeout(resolve, 50))
        selections.push(count())
      }
      results.push({ progressive, before, selections })
      chart.dispose()
    }
    return results
  })
  console.log(JSON.stringify(results, null, 2))
  assert.equal(results[1].before, 12345)
  assert.deepEqual(results[1].selections, [12345, 12345, 12345])
} finally {
  await browser.close()
}
