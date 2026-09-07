# Phase 0 작업계획 — 기준선·구조 조사

## 목표

기존 Vue 프런트엔드의 라우트, 상태, API, 화면 동작, 성능을 React 이전의 기준선으로 고정한다.

## 작업

1. `EALO/frontend/src/router.js` 전체 라우트와 가드를 목록화한다.
2. `src/vuex/store.js`, `common.js`, `EventBus.js`의 상태·액션·이벤트를 도메인별로 분류한다.
3. 화면별 API URL, method, request/response, 오류 처리 위치를 기록한다.
4. Init, Lookup, Detail, Analysis, Comparison, 관리 화면의 대표 fixture를 만든다.
5. 로그인, 권한, 세션 만료, 업로드, 팝업, 다운로드 흐름을 기록한다.
6. 동일 fixture에 대한 Vue의 수치·화면·성능을 측정한다.
7. Raw Log의 개인정보·민감 필드와 브라우저 노출/마스킹 정책을 분류한다.
8. React 전환에 필요한 백엔드 API 변경을 프런트 작업과 분리해 백엔드 인계 목록으로 만든다.
9. AG Grid Community/Enterprise, 서버 상태 캐시, 전역 UI 상태, 인증 방식, API 버전 전략을 의사결정 목록으로 확정한다.

## 산출물

- `route-matrix.md`
- `state-and-event-matrix.md`
- `api-contract-inventory.md`
- `fixtures/`
- `baseline-report.md`
- `security-and-data-classification.md`
- `backend-handoff.md`
- `decision-log.md`

진행 상태: 완료. 구조 조사·API 호출 매핑·fixture·Vue/Django root 및 DB 의존 endpoint smoke·HTTP 기준 측정을 완료했다.
