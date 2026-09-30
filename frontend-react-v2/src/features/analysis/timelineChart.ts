export type TimedPoint = [number, number | null]

function timelineDigits(value: unknown) {
  return String(value ?? '').replace(/\D/g, '')
}

export function timelineStepMs(values: unknown[]) {
  const length = Math.max(0, ...values.map((value) => timelineDigits(value).length))
  if (length >= 14) return 1_000
  if (length >= 12) return 60_000
  return 3_600_000
}

export function timelineTimestamp(value: unknown) {
  const digits = timelineDigits(value)
  if (digits.length < 10) return null
  const parts = [
    Number(digits.slice(0, 4)),
    Number(digits.slice(4, 6)),
    Number(digits.slice(6, 8)),
    Number(digits.slice(8, 10)),
    digits.length >= 12 ? Number(digits.slice(10, 12)) : 0,
    digits.length >= 14 ? Number(digits.slice(12, 14)) : 0,
  ]
  const timestamp = new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5]).getTime()
  return Number.isFinite(timestamp) ? timestamp : null
}

export function formatAxisTimestamp(value: number) {
  const date = new Date(value)
  const pad = (part: number) => String(part).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}\n${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}

/**
 * Convert sparse buckets to real timestamps so elapsed time controls spacing.
 * Missing buckets are represented by zero-valued edge points. Two points are
 * enough for a long gap, so a multi-day second-level query does not create
 * millions of synthetic data items.
 */
export function timedSeries(labels: unknown[], values: Array<number | null | undefined>): TimedPoint[] {
  const result: TimedPoint[] = []
  const step = timelineStepMs(labels)
  let previous: number | null = null

  labels.forEach((label, index) => {
    const timestamp = timelineTimestamp(label)
    if (timestamp === null) return
    if (previous !== null && timestamp - previous > step) {
      const gapStart = previous + step
      const gapEnd = timestamp - step
      result.push([gapStart, 0])
      if (gapEnd > gapStart) result.push([gapEnd, 0])
    }
    result.push([timestamp, values[index] ?? null])
    previous = timestamp
  })
  return result
}

export function showTimelineSymbols(labels: unknown[]) {
  // A single point has no line segment. A modest number of sparse points also
  // benefits from markers, while dense charts remain uncluttered and fast.
  if (labels.length <= 1) return true
  if (labels.length > 1_000) return false
  const step = timelineStepMs(labels)
  let previous: number | null = null
  for (const label of labels) {
    const timestamp = timelineTimestamp(label)
    if (timestamp === null) continue
    if (previous !== null && timestamp - previous > step) return true
    previous = timestamp
  }
  return false
}
