import { expect, it } from 'vitest'
import { combineRequestTime } from './requestTimeChart'

it('preserves TPS values and aligns response time by timestamp', () => {
  expect(combineRequestTime(
    { resultX: ['202609100901', '202609100902', '202609100903'], resultY: [1.2, 3.4, 5.6] },
    { resultX: ['202609100903', '202609100901'], resultY: [336, 72], resultY_time: [0.8, 0.2] },
  )).toEqual({
    resultX: ['202609100901', '202609100902', '202609100903'],
    resultY: [1.2, 3.4, 5.6], resultY_time: [0.2, null, 0.8],
  })
})

it('retains TPS when the log format has no response time', () => {
  expect(combineRequestTime({ resultX: ['20260910'], resultY: [10] }, {}).resultY_time).toEqual([null])
  expect(combineRequestTime({}, {}).resultY_time).toEqual([])
})
