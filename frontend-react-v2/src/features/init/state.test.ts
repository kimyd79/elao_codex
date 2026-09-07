import { describe, expect, it } from 'vitest'
import { initialInitState, moveStep } from './state'
describe('init step state machine', () => {
  it('moves within valid range', () => {
    expect(moveStep(initialInitState, 1).step).toBe('step1')
    expect(moveStep(initialInitState, -1).step).toBe('current')
    expect(moveStep({ ...initialInitState, step: 'step3' }, 1).step).toBe('step3')
  })
})
