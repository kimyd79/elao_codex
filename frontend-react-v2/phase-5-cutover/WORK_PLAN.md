# Phase 5 작업계획 — 통합 검증·병행 운영·전환

## 목표

React v2의 기능·수치·성능·접근성·운영 안정성을 검증하고 라우트 단위로 전환한다.

## 작업

1. Playwright로 로그인부터 초기화·조회·분석·비교 여정을 자동화한다.
2. Vue/React fixture 비교와 시각 회귀 캡처를 실행한다.
3. Chrome/Edge, 키보드, 포커스, 대비, 반응형 최소 폭을 검증한다.
4. API p50/p95, 오류율, 취소율, 표 스크롤, 차트 응답시간을 수집한다.
5. Docker/static hosting/reverse proxy smoke test를 실행한다.
6. feature flag와 health check로 Vue 롤백을 보장한다.
7. 승인 후 라우트 단위로 React 기본 진입점을 전환한다.
8. 안정화 후 Lego/Vue 제거 여부를 별도 승인한다.
9. API/DB 하위 호환 기간, feature flag 제거 시점, 데이터·로그 보존 기간을 확정한다.
10. 운영 인수인계와 장애 대응 훈련을 수행한다.

## 산출물

- E2E/시각 회귀 결과
- 성능·오류 지표 보고서
- 배포·롤백 runbook
- 라우트별 전환 승인표
- 운영 인수인계 체크리스트와 flag 제거 계획
