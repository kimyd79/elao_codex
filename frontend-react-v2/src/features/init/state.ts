export const initSteps = ['current', 'step1', 'step2', 'step3'] as const
export type InitStep = (typeof initSteps)[number]
export type InitState = {
  step: InitStep
  projectMode: 'new' | 'existing'
  addLogFiles: boolean
  projectName: string
  projectDescription: string
  projectId: string
  serverName: string
  instanceName: string
  logFormat: string
  range: 'all' | 'select'
}
export const initialInitState: InitState = {
  step: 'current',
  projectMode: 'new',
  addLogFiles: false,
  projectName: '',
  projectDescription: '',
  projectId: '',
  serverName: '',
  instanceName: '',
  logFormat: '',
  range: 'all',
}
export function stepIndex(step: InitStep) {
  return initSteps.indexOf(step)
}
export function moveStep(state: InitState, direction: -1 | 1): InitState {
  const next = stepIndex(state.step) + direction
  return next < 0 || next >= initSteps.length ? state : { ...state, step: initSteps[next] }
}
