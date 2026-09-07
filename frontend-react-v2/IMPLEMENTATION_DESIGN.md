# React 프런트엔드 v2 단계별 실행 설계

이 문서는 `PLAN.md`를 실제 개발 작업으로 분해한 실행 설계서다. 기존 `EALO/frontend` Vue 애플리케이션은 모든 단계에서 보존한다.

## 공통 원칙

- 각 Phase 종료 시 독립적으로 설치·빌드·실행 가능해야 한다.
- 화면에서 직접 API를 호출하지 않고 typed adapter와 fixture를 사용한다.
- 화면 동등성, 수치 동등성, 성능을 별도로 검증한다.
- feature flag로 Vue/React를 선택하고 실패 시 Vue로 롤백한다.

## Phase 0 — 기준선 및 계약 조사

### 작업

1. `router.js` 전체 라우트·가드·메뉴 전환을 표로 작성한다.
2. `vuex/store.js`, `common.js`, `EventBus.js`의 상태·액션·이벤트를 도메인별로 분류한다.
3. 화면별 API URL, method, 요청 필드, 응답 변환, 오류 처리 위치를 기록한다.
4. Init/Lookup/Detail/Analysis/Comparison/관리 화면의 대표 fixture를 고정한다.
5. 로그인, 권한, 세션 만료, 업로드, 팝업, 다운로드의 기준 동작을 캡처한다.
6. 동일 데이터로 Vue 수치·화면·성능 기준을 측정한다.

### 산출물과 완료 조건

- `route-matrix.md`, `state-and-event-matrix.md`, `api-contract-inventory.md`
- `fixtures/` 요청·응답·로그 데이터
- 모든 라우트가 이전·제외·보류 중 하나로 분류됨
- 동일 fixture로 Vue 결과를 재현할 수 있음

## Phase 1 — React 실행 기반

### 작업

1. React + TypeScript + Vite를 구성하고 Node/npm과 환경변수를 고정한다.
2. ESLint, Prettier, typecheck, Vitest, Playwright를 구성한다.
3. Tailwind/shadcn/ui와 dense 디자인 토큰을 정의한다.
4. AppShell, ErrorBoundary, Loading/Empty/Error 상태를 구현한다.
5. API client에 base URL, timeout, request id, 인증, 오류 정규화, AbortSignal을 구현한다.
6. React Router, 인증 provider, 권한 가드, 세션 만료 redirect를 구현한다.
7. CI에서 lint/typecheck/unit/build를 실행한다.

### 완료 조건

- 빈 앱이 독립적으로 실행·빌드됨
- 로그인 전후 가드와 만료 세션 처리가 동작함
- 잘못된 API와 빈 응답이 공통 상태로 표시됨

## Phase 2 — AppShell·인증·탭·초기화

### 작업

1. `/`, `/login`, `/logout`, `/register`, `/initialization`을 이전한다.
2. AppShell, 상단/사이드 메뉴, 현재 메뉴 표시를 구현한다.
3. `Init.vue`의 `tabs[].isSelected`를 명시적 단계 상태로 변환한다.
4. 이전/다음/삭제/새 프로젝트와 조건부 단계 표시를 이전한다.
5. 프로젝트·서버·인스턴스·로그 포맷·업로드 진행/취소/재시도를 구현한다.
6. 탭 상태를 URL route/query와 동기화한다.

### 완료 조건

- Init 핵심 시나리오가 동일한 순서와 결과로 동작함
- 새로 고침 후 URL로 현재 화면을 복원함
- 장시간 업로드를 취소하고 실패 후 재시도할 수 있음

## Phase 3 — 관리·Lookup·Detail·AG Grid

### 작업

1. `/project`, `/logformat`, `/metrics`를 이전한다.
2. Lookup 필터를 typed model로 정의하고 검색어·제외어·전후 라인을 API query로 변환한다.
3. AG Grid adapter에 컬럼, 정렬, 선택, 상세 팝업, 다운로드를 연결한다.
4. cursor pagination, 필터 변경 시 cursor 초기화, 중복 행 방지를 구현한다.
5. Detail에서 선택 행의 원본·전후 문맥을 지연 조회한다.
6. 10만·100만·수백만 건으로 가상화·메모리를 측정한다.

### 완료 조건

- 전체 Raw Log를 브라우저로 받지 않음
- 정렬·필터·상세 조회가 일관됨
- 기준선 대비 메모리·스크롤 목표를 충족함

## Phase 4 — Analysis·Comparison·ECharts

### 작업

1. `/analysis`, `/comparison_chart`, `/comparison_statistic`을 이전한다.
2. Chart.js 지표·조건을 metric/group-by 모델로 정규화한다.
3. 시간 범위, HH/HHMM/HHMMSS, timezone, 필터를 API 요청으로 변환한다.
4. ECharts wrapper에 resize/dispose/loading/empty/error/tooltip/legend를 구현한다.
5. DataZoom, 서버 집계, 구간 샘플링을 조합한다.
6. 차트 클릭으로 상세 통계·Raw Log를 조회한다.
7. 동일 fixture의 합계·평균·비율·시간 경계를 Vue와 비교한다.

### 완료 조건

- 핵심 수치가 Vue 결과와 일치함
- 확대·축소·범례·재조회가 안정적임
- 브라우저 메모리와 렌더링 데이터가 제한됨

## Phase 5 — 통합 검증·병행 운영·전환

### 작업

1. Playwright로 로그인부터 초기화·조회·분석·비교 여정을 자동화한다.
2. Vue/React fixture 비교와 시각 회귀 캡처를 실행한다.
3. Chrome/Edge, 키보드 탐색, 포커스, 대비, 반응형 최소 폭을 검증한다.
4. API p50/p95, 오류율, 취소율, 표 스크롤, 차트 응답시간을 수집한다.
5. Docker/static hosting/reverse proxy smoke test를 실행한다.
6. feature flag와 health check로 Vue 롤백을 보장한다.
7. 승인 후 라우트 단위로 React 기본 진입점을 전환한다.
8. 안정화 후 Lego/Vue 제거 여부를 별도 승인한다.

### 완료 조건

- 기능·수치·성능·접근성·배포 검증을 모두 통과함
- React 장애 시 Vue로 복귀 가능함
- 기존 Vue/Lego 삭제가 기능 전환과 분리됨

## 의존성

```text
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
                    └──────────────→ Phase 5
```

Phase 1은 환경변수·인증·API 계약, Phase 3/4는 fixture와 시간 의미 정의가 필요하다. Phase 5는 Phase 2~4의 핵심 시나리오 완료 후 시작한다.

## 정량 게이트

초기 목표값은 Phase 0 측정 후 확정한다. Vue 기준선 대비 첫 화면, 탭 전환, API p95, 10만/100만 행 스크롤, 차트 DataZoom, 브라우저 메모리, E2E 성공률, JavaScript 오류율을 기록하고 비교한다.
