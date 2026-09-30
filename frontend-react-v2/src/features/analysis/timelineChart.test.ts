import { expect, it } from 'vitest'
import { showTimelineSymbols, timedSeries, timelineStepMs, timelineTimestamp } from './timelineChart'

it('uses elapsed time rather than data density for minute buckets', () => {
  const labels = ['202609220900', '202609220901', '202609221001']
  const points = timedSeries(labels, [1, 2, 3])

  expect(timelineStepMs(labels)).toBe(60_000)
  expect(timelineTimestamp(labels[1])! - timelineTimestamp(labels[0])!).toBe(60_000)
  expect(timelineTimestamp(labels[2])! - timelineTimestamp(labels[1])!).toBe(3_600_000)
  expect(points).toEqual([
    [timelineTimestamp(labels[0])!, 1],
    [timelineTimestamp(labels[1])!, 2],
    [timelineTimestamp('202609220902')!, 0],
    [timelineTimestamp('202609221000')!, 0],
    [timelineTimestamp(labels[2])!, 3],
  ])
  expect(showTimelineSymbols(labels)).toBe(true)
})

it('shows missing second buckets as zero without filling every empty bucket', () => {
  expect(timelineStepMs(['2026092209'])).toBe(3_600_000)
  expect(timelineStepMs(['20260922090001'])).toBe(1_000)
  expect(timedSeries(['20260922090001', '20260922090003'], [4, 5])).toEqual([
    [timelineTimestamp('20260922090001')!, 4],
    [timelineTimestamp('20260922090002')!, 0],
    [timelineTimestamp('20260922090003')!, 5],
  ])
  expect(showTimelineSymbols(['20260922090001', '20260922090003'])).toBe(true)
  expect(showTimelineSymbols(['20260922090001'])).toBe(true)
})
