# ELAO React Frontend v2

대용량 로그 조회와 분석을 위한 React 기반 차세대 프런트엔드 작업 영역입니다.

기존 `frontend`(Vue 2.7 + Lego)는 병행 운영하며, v2가 기능·성능 검증을 통과한 뒤 단계적으로 전환합니다.

## 목표 구조

```text
React + shadcn/ui
       |
  Tab application shell
       |
  AG Grid / ECharts
       |
  API client
       |
  Django aggregation and cursor-paging APIs
```

전체 단계 계획은 [PLAN.md](./PLAN.md), 작업 단위·산출물·검증 게이트는 [IMPLEMENTATION_DESIGN.md](./IMPLEMENTATION_DESIGN.md)에 기록합니다.

## 단계별 실행 문서

- `phase-0-baseline/`: 기준선·라우트·상태·API 조사
- `phase-1-foundation/`: React 실행 기반·공통 UI·API client
- `phase-2-shell-init/`: AppShell·인증·탭·초기화
- `phase-3-data-grid/`: 관리·Lookup·Detail·AG Grid
- `phase-4-charts/`: Analysis·Comparison·ECharts
- `phase-5-cutover/`: 통합 검증·병행 운영·전환

각 단계 폴더에는 `WORK_PLAN.md`, `VERIFICATION.md`, `METHOD.md`가 있습니다.
