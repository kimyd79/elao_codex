import { expect, it } from 'vitest'
import { statisticCondition } from './StatisticDetailDialog'

it('maps every statistics table to the legacy detail condition field', () => {
  expect(statisticCondition(1)).toEqual({ code: 'S', label: 'Status' })
  expect(statisticCondition(2)).toEqual({ code: 'R', label: 'Request' })
  expect(statisticCondition(3)).toEqual({ code: 'NFR', label: 'Request (404)' })
  expect(statisticCondition(5)).toEqual({ code: 'I', label: 'IP' })
  expect(statisticCondition(6)).toEqual({ code: 'E', label: 'Referrer' })
  expect(statisticCondition(7)).toEqual({ code: 'U', label: 'UserAgent' })
  expect(statisticCondition(9)).toEqual({ code: 'F', label: 'Static file type' })
  expect(statisticCondition(13)).toEqual({ code: 'V1', label: 'Upstream' })
  expect(statisticCondition(14)).toEqual({ code: 'V2', label: 'Domain' })
})
