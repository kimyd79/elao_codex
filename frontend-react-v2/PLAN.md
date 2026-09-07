# ELAO React 프런트엔드 2차 구축 계획

작성일: 2026-08-13  
상태: 계획 수립 및 기반 조사

## 1. 목적

기존 Vue 2.7/Lego 화면을 즉시 삭제하지 않고 별도 React 애플리케이션으로 재구축한다. 현재 탭 구조와 업무 흐름은 유지하면서, 수백만 건 로그를 브라우저에 전부 전달하지 않는 서버 집계·커서 페이징 기반의 촘촘한 UI를 제공한다.

## 2. 범위

### 포함

- React 기반 애플리케이션 셸과 현재 탭 구조 이전
- shadcn/ui + Tailwind CSS 기반의 조밀한 디자인 토큰
- AG Grid 기반 Raw Log/검색 결과 표
- ECharts 기반 분석·비교 차트
- API client, 요청 취소, 오류·빈 결과·로딩 상태 표준화
- 서버 집계, 커서 페이징, 차트 샘플링 API 연계
- 기존 Vue 화면과 결과를 비교하는 회귀 검증

## 2.1 기존 프런트엔드 기준선

React v2는 기존 화면을 새로 발명하지 않고 현재 Vue 애플리케이션의 동작 계약을 이전한다. 조사 결과 기준선은 다음과 같다.

- 기존 앱: `EALO/frontend`, Vue 2.7.16, Vue Router 3, Vuex 3, Vue CLI 5/Webpack 5
- 전역 등록: `src/main.js`에서 `Vue.use(LegoComponent)` 및 `src/components/layout/index.js`의 `ui-*` 컴포넌트 등록
- Lego 사용: 약 107개 소스 파일, 약 1,014개 템플릿 태그 사용
- 주요 Lego 의존: button, icon, text-field, dropdown, radio, checkbox, date-picker, pagination, tree, segment, tab
- 주요 업무 화면: `Init.vue`, `Lookup.vue`, `Analysis.vue`, `Comparison.vue`, `ComparisonStatistic.vue`
- 추가 라우트: `/detail`, `/management`, `/logformat`, `/project`, `/metrics`, `/login`, `/logout`, `/register`, `/test`
- 인증/라우팅: `src/router.js`의 로그인·관리자 가드와 `src/vuex/store.js` 전역 상태를 이전해야 함
- 초기화 탭: `Init.vue`가 `tabs[].isSelected`, `tabChange`, 이전/다음 단계 로직으로 화면 단계를 제어
- 공통 탭: `src/components/layout/tab/UITab.vue`가 `tabs` 배열을 받아 box/underline/removable 스타일을 렌더링
- Lego 탭: 샘플·레이아웃 화면에서 `lego-tab-box`와 `lego-tab-label`을 직접 사용
- 공통 표: `ui-table` 래퍼가 여러 업무 화면에서 사용되므로 React에서는 AG Grid 어댑터로 기능을 보존

이 기준선은 화면별 이전 순서와 회귀 테스트 항목의 원본으로 사용한다. 특히 `Init.vue`의 단계 전환은 단순 탭 UI 교체가 아니라 상태 머신으로 명시해야 한다.

### 이전 대상 우선순위

1. 인증·AppShell·메뉴 가드: 로그인, 로그아웃, 권한, 세션 만료
2. 초기화·프로젝트·로그 포맷·메트릭 관리
3. Lookup·Detail 원본 로그 조회
4. Analysis·Comparison·ComparisonStatistic 분석 화면
5. 개발용 `/test`와 Lego 디자인 샘플은 제품 전환 대상에서 제외하거나 별도 검증 화면으로 유지

### 제외

- 이번 단계에서 Django 로그 적재 파이프라인 자체를 재작성하지 않음
- 기존 Vue 프런트엔드를 먼저 삭제하지 않음
- Raw Log 수백만 건을 한 번에 내려받는 기능을 만들지 않음
- AG Grid Enterprise 구매를 전제로 하지 않음(Community + 자체 커서 API를 우선 검토)

## 3. 기준 아키텍처

```text
frontend-react-v2/
├─ src/
│  ├─ app/              # 라우팅, 전역 상태, 오류 경계
│  ├─ components/       # shadcn/ui 및 공통 업무 컴포넌트
│  ├─ features/
│  │  ├─ init/          # 프로젝트/로그 포맷 초기화
│  │  ├─ lookup/        # Raw Log 검색 및 AG Grid
│  │  ├─ analysis/      # 단일 로그 분석 및 ECharts
│  │  └─ comparison/    # 로그 비교 및 ECharts
│  ├─ layouts/          # AppShell, Sidebar, TabLayout
│  ├─ lib/              # API client, 포맷터, 검증
│  └─ styles/           # dense 토큰, 테마
├─ tests/
└─ PLAN.md
```

## 4. 탭 호환 원칙

현재 `Init`, `Analysis`, `Comparison`, `Lookup` 탭의 라벨·순서·권한·업무 전환을 보존한다. 탭 상태는 URL 라우트와 화면 상태를 분리한다.

- URL: 현재 탭, 프로젝트, 로그 파일 식별자
- 화면 상태: 필터, 정렬, 커서, 차트 시간 구간
- 탭 전환 시 필터와 차트 상태를 복원할 수 있도록 feature 단위로 상태를 보관
- 초기화 화면의 이전/다음 단계와 `tabs[].isSelected` 의미를 React 상태 머신으로 명시

## 5. API 계약 초안

기존 API는 화면별 POST/GET 호출과 응답 변환이 `common.js` 및 각 Vue 컴포넌트에 분산되어 있다. 새 API를 추가하기 전에 기존 엔드포인트, 인증 방식, 오류 형식, 날짜·시간대 의미를 표로 고정하고 React API client에서만 호출하도록 한다.

### Raw Log

`GET /api/logs`

- `project_id`, `logfile_id`
- `cursor`, `limit`, `sort`
- 검색어, 제외어, 전후 라인 조건
- 응답: `items`, `next_cursor`, `has_more`, `columns`

### 시계열 집계

`GET /api/analysis/timeseries`

- `start`, `end`, `interval`, `metric`, 필터
- 응답: 구간별 집계값, 원본 건수, 적용된 샘플링 방식

### 분류 집계

`GET /api/analysis/breakdown`

- `group_by`, `top_n`, 필터
- 응답: 상위 항목, 기타 합계, 전체 건수

서버가 집계·샘플링하고, 브라우저는 화면에 필요한 점과 행만 렌더링한다. API 확정 전에는 프런트에 임시 어댑터를 두어 실제 응답과 목 응답을 동일한 타입으로 취급한다.

### 공통 계약

- 인증: 세션/쿠키 또는 토큰 방식, CSRF, CORS, 만료 시 `/login` 이동
- 오류: HTTP 상태·백엔드 오류 코드·사용자 메시지·재시도 가능 여부
- 시간: 저장 시간대, 표시 시간대, 경계 포함 여부, HH/HHMM/HHMMSS 집계 규칙
- 목록: `next_cursor`, 정렬 안정성, 필터 변경 시 커서 초기화
- 업로드: 진행률, 취소, 재시도, 중복 제출 방지

## 6. 단계별 실행 계획

### Phase 0 — 기준선 고정

- 기존 Vue의 초기화·조회·분석·비교 핵심 시나리오와 화면 캡처 확보
- 현재 API 응답 및 탭 상태 전이 기록
- `lego-*`와 `ui-*` 컴포넌트의 props/events/slot 사용표 작성
- 화면별 라우트, Vuex 상태, 팝업, 차트·표 데이터 변환 로직 매핑
- 성능 기준 측정: 첫 화면 시간, 10만 행 스크롤, 차트 확대/축소 응답시간
- 인증·권한·세션 만료, 파일 업로드/진행률, 팝업/다운로드 흐름을 별도 기준선으로 기록
- 브라우저 지원 범위와 운영 배포 방식(Docker/static hosting, reverse proxy, 환경변수)을 확정

완료 기준: Vue 기준선과 테스트 데이터가 재현 가능하고, 각 React feature의 이전 대상과 호환성 차이가 문서화됨.

### Phase 1 — React 기반 구축

- React + TypeScript + Vite 구성
- Tailwind/shadcn/ui 설치 및 dense 디자인 토큰 정의
- ESLint, formatter, 테스트 러너, 환경변수 규칙 구성
- AppShell, 오류 경계, API client, 로딩/오류/빈 상태 구축
- React Router, 서버 상태 캐시/요청 취소, 인증 provider, 권한 가드 구축
- CI에서 lint/typecheck/unit/build를 실행하고 Node/npm 버전을 고정

완료 기준: 빈 탭 셸이 독립적으로 실행·빌드되고 기존 백엔드에 연결됨.

### Phase 2 — 탭과 초기화 화면

- `Init.vue`의 탭 배열·단계 전환·이전/다음·조건부 영역을 React 상태 머신으로 이전
- 현재 탭 라우트 및 선택 상태 이전
- Init 단계 전환, 이전/다음, 검증 메시지 이전
- 공통 버튼·입력·선택·날짜 컴포넌트 구현

완료 기준: 기존 Init 핵심 시나리오가 동일한 순서와 결과로 동작함.

### Phase 3 — Lookup과 AG Grid

- 서버 커서 페이징과 필터/정렬 연결
- AG Grid 행 가상화, 컬럼 상태, 로딩 오버레이 적용
- 검색어·제외어·전후 라인 조건 지원

완료 기준: 대용량 데이터에서 브라우저 메모리와 스크롤 성능이 기준선보다 개선됨.

### Phase 4 — Analysis/Comparison과 ECharts

- 서버 시계열 집계 및 분류 집계 연동
- DataZoom, tooltip, 범례, 시간 해상도 전환
- 서버/클라이언트 샘플링과 포인트 수 제한
- 기존 Chart.js 결과와 수치 비교

완료 기준: 동일 조건에서 수치가 일치하고 확대·축소가 안정적으로 동작함.

### Phase 5 — 병행 운영과 전환

- 기존 Vue 링크와 React v2 링크 병행 제공
- 사용자 시나리오 및 브라우저 회귀 테스트
- 오류율, API 응답시간, 표/차트 성능 모니터링
- 접근성(키보드 탭 이동, 포커스, 색상 대비), 반응형 최소 기준, 브라우저 회귀 검증
- 배포별 feature flag와 즉시 Vue로 되돌리는 롤백 경로 운영
- 전환 승인 후 기본 진입점을 React로 변경

완료 기준: 핵심 기능 동등성, 성능 기준, 롤백 절차가 모두 확인됨.

## 7. 위험과 대응

| 위험                    | 대응                                                              |
| ----------------------- | ----------------------------------------------------------------- |
| Vue와 React 기능 차이   | 화면 단위로 이전하고 API 결과를 비교                              |
| 서버 집계 API 지연      | 인덱스·집계 구간·캐시를 별도 측정                                 |
| 대용량 표 메모리 증가   | 서버 커서, 행 가상화, 컬럼 수 제한                                |
| 차트 데이터 과다        | 시간 간격 자동 조정, LTTB/구간 집계                               |
| shadcn 스타일 불일치    | 토큰과 공통 래퍼를 먼저 고정                                      |
| AG Grid Enterprise 비용 | Community + 자체 API 페이징을 우선 검증                           |
| 병행 운영 복잡성        | 기존 Vue는 변경을 최소화하고 v2 API 계약을 독립 관리              |
| 인증·세션 차이          | 로그인/로그아웃/만료/권한 가드를 Phase 1에서 먼저 검증            |
| 기존 라우트 누락        | 전체 라우트 매트릭스와 이전 우선순위를 기준선 문서로 유지         |
| 시간대·집계 의미 불일치 | 대표 로그 fixture로 날짜 경계와 HH/HHMM/HHMMSS 수치를 계약 테스트 |
| 업로드·장시간 작업 중단 | 진행률·취소·재시도·중복 방지 상태를 공통 작업 모델로 구현         |
| 운영 설정 오류          | `.env` 스키마 검증, Docker/reverse-proxy smoke test, feature flag |
| 접근성·브라우저 회귀    | 키보드·대비·지원 브라우저 자동/수동 검증                          |

## 8. 완료 정의

- React v2가 독립적으로 설치·빌드·실행됨
- 현재 Init/Lookup/Analysis/Comparison 탭과 주요 업무 흐름이 유지됨
- 수백만 건 원본을 브라우저로 직접 전송하지 않음
- Raw Log는 서버 커서 페이징과 AG Grid 가상화로 조회됨
- 차트는 서버 집계·샘플링과 ECharts DataZoom으로 조회됨
- 기존 Vue와 수치·권한·오류 처리 결과가 검증됨
- 롤백을 위해 기존 Vue 진입점이 유지됨
- 전체 제품 라우트의 이전/제외 사유가 문서화됨
- 인증, 권한, 업로드, 오류, 시간대, 접근성, 배포 smoke test가 통과함
- 정량 성능 기준(초기 로딩, API p95, 표 스크롤, 차트 상호작용)이 기준선 대비 충족됨

## 9. 다음 작업

1. 전체 라우트·Vuex 상태·API 호출 매트릭스 작성
2. Phase 0 기준선 측정과 대표 로그 fixture 수집
3. 인증/세션/업로드/시간대 API 계약 확정
4. React/Vite/TypeScript 기반 파일 생성
5. AppShell 및 탭 라우트 구현
6. 백엔드 API 계약을 문서와 계약 테스트로 고정
