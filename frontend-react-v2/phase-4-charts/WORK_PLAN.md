# Phase 4 작업계획 — Analysis·Comparison·ECharts

## 목표

분석·비교 차트를 서버 집계와 ECharts DataZoom 기반으로 이전한다.

## 작업

1. `/analysis`, `/comparison_chart`, `/comparison_statistic`을 이전한다.
2. Chart.js 지표·조건을 metric/group-by 모델로 정규화한다.
3. 시간 범위, HH/HHMM/HHMMSS, timezone, 필터를 API 요청으로 변환한다.
4. ECharts wrapper에 resize/dispose/loading/empty/error/tooltip/legend를 구현한다.
5. 서버 집계, 시간 구간 자동 조정, LTTB/구간 샘플링, DataZoom을 조합한다.
6. 차트 클릭으로 상세 통계·Raw Log를 조회한다.
7. 동일 fixture의 합계·평균·비율·시간 경계를 Vue와 비교한다.
8. 차트 색상 대비, 키보드 대체 정보, 데이터 표/다운로드 제공 여부를 설계한다.
9. 집계 캐시 키, stale 응답 폐기, 재조회 취소 정책을 확정한다.

## 산출물

- `src/features/analysis`, `comparison`
- chart option builder와 metric adapter
- 수치 동등성 계약 테스트
- 차트 성능 보고서
- 차트 접근성·캐시·stale 응답 검증 결과
