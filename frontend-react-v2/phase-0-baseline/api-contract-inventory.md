# API 계약 인벤토리

## 백엔드 라우트 기준

출처: `EALO/backend/loganalyzerapi/urls.py`의 DRF router.

| 리소스           | 기본 경로                       | 용도                  | React 대상 |
| ---------------- | ------------------------------- | --------------------- | ---------- |
| LogMaster        | `/mwla/logmaster/`              | 프로젝트              | Phase 2/3  |
| LogFile          | `/mwla/logfile/`                | 로그 파일·업로드      | Phase 2/3  |
| LogAnalysisJob   | `/mwla/loganalysisjob/`         | 비동기 분석 작업 상태 | Phase 2/4  |
| LogDetailV2      | `/mwla/logdetail_v2/`           | 신규 상세 로그        | Phase 3    |
| DynamicLogDetail | `/mwla/logdetail_dynamic/`      | 동적 상세/기존 조회   | Phase 3    |
| LogFormat        | `/mwla/logformat/`              | 로그 포맷             | Phase 2/3  |
| LogFormatString  | `/mwla/logformatstring/`        | 포맷 문자열           | Phase 2/3  |
| User             | `/mwla/user/`                   | 사용자                | Phase 2    |
| Metrics          | `/mwla/metrics/`                | 메트릭                | Phase 3/4  |
| LogMasterMetric  | `/mwla/logmastermetric/`        | 프로젝트-메트릭 연결  | Phase 3/4  |
| Auth             | `/mwla/rest-auth/`              | 로그인·로그아웃       | Phase 1/2  |
| Registration     | `/mwla/rest-auth/registration/` | 사용자 등록           | Phase 2    |

## 커스텀 action 엔드포인트

| 경로                                          | method | 호출 위치/용도        |
| --------------------------------------------- | ------ | --------------------- |
| `/logdetail_dynamic/statistics/`              | POST   | 단일 통계 집계        |
| `/logdetail_dynamic/chartdata/`               | POST   | 단일 차트 데이터      |
| `/logdetail_dynamic/chartdata_diff/`          | POST   | 비교 차트 데이터      |
| `/logdetail_dynamic/get_before_after_detail/` | POST   | 전후 문맥             |
| `/logdetail_dynamic/start_end/`               | POST   | 로그 시작·종료 범위   |
| `/logdetail_dynamic/findings/`                | POST   | findings 조회         |
| `/logdetail_dynamic/uridetail/`               | POST   | URI 상세 통계         |
| `/logmaster/create_dynamic_logdetail/`        | POST   | 동적 상세 테이블/적재 |
| `/logmaster/delete_dynamic_logdetail/`        | POST   | 동적 상세 삭제        |
| `/logformat/assist/`                          | POST   | 로그 포맷 보조        |
| `/logformatstring/formatkind_list/`           | GET    | 포맷 종류 목록        |

## 계약 위험

- 기존 화면에는 `/logfile?project=...`, `/logmaster?...`처럼 trailing slash가 없는 호출도 있어 Django `APPEND_SLASH`와 프록시 동작을 확인해야 한다.
- 현재 조회는 `limit`/`offset` 페이지 방식이 사용되며, React 목표의 cursor 방식과 병행 API 또는 서버 어댑터가 필요하다.
- 차트·통계 요청은 `common.js`에서 type 숫자와 문자열 필터를 조립하므로 metric enum/응답 schema를 먼저 고정해야 한다.

## 기존 프런트 호출 기준

- 기본 API URL: `VUE_APP_API_URL` 또는 `http://127.0.0.1:8000/mwla`
- 호출이 `common.js`와 개별 `.vue` 파일에 분산되어 있으므로 endpoint 목록만으로 완료 처리하지 않는다.
- `getSearchFilter`, `getDetailSearchFilter`, `setCommonStatisticInfo`를 React typed query builder로 분리한다.

## 계약 확정 필요

인증 쿠키/토큰·CSRF, 페이지네이션 방식, 오류 JSON, 시간대, 업로드 진행률, 분석 작업 상태, Raw Log 마스킹, 다운로드 API를 백엔드와 확정한다.
