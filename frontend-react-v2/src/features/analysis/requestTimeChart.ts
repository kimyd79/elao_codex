import type { ChartPayload } from './service'

// Join by the raw timestamp, not array position: missing time values must not
// shift onto another TPS bucket or appear as zero response time.
export function combineRequestTime(tps: ChartPayload, time: ChartPayload): ChartPayload {
  const times = new Map((time.resultX ?? []).map((x, index) => [x, time.resultY_time?.[index] ?? null]))
  return {
    ...tps,
    resultY_time: (tps.resultX ?? []).map((x) => times.get(x) ?? null),
  }
}
