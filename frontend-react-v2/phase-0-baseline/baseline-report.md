# Phase 0 기준선 보고서

상태: 측정 전 템플릿

2026-08-13 정적 기준선: 이 작업 시점에 8000/8080/8081 포트에서 실행 중인 프로세스가 없어 브라우저 Network·성능 측정은 아직 수행하지 않았다. 서버 기동 후 동일한 fixture와 브라우저에서 측정한다.

기존 백엔드 로그 정적 점검에서 `statistics`, `chartdata`, `findings` 처리 중 `NoneType` iterable 및 `totalCnt` 미할당 오류가 확인되었다. React 전환 성능 측정 전에 동일 조건의 오류 재현 여부와 API 오류 응답 계약을 먼저 확인한다.

2026-08-14 런타임 smoke 결과는 [runtime-smoke-report.md](./runtime-smoke-report.md)에 기록했다. Vue와 Django root는 200 응답했으나 DB가 필요한 API 검증은 PostgreSQL UTF-8 연결 오류로 보류했다.

후속 재실행에서 PostgreSQL이 5432 포트에 정상 청취했고 `/mwla/`, `/mwla/logmaster/`, `/mwla/logfile/`, Vue `/`가 모두 HTTP 200을 반환했다. 응답 시간은 `tools/runtime-check.json`에 기록했다.

### 2026-08-14 HTTP 기준 측정 (각 3회)

| endpoint               | status | median ms | p95 ms | bytes |
| ---------------------- | -----: | --------: | -----: | ----: |
| `GET /mwla/`           |    200 |     50.95 |  92.62 |   559 |
| `GET /mwla/logmaster/` |    200 |    137.97 | 139.15 |   411 |
| `GET /mwla/logfile/`   |    200 |    136.81 | 150.86 |  1496 |
| `GET frontend /`       |    200 |     32.10 |  33.49 |   677 |

측정 도구: `tools/run-runtime-check.ps1`, 상세 원자료: `tools/runtime-check.json`.

## 실행 환경

- Vue frontend commit/worktree: `git-status.txt` 기준
- Node/npm: 기록 필요
- Browser/OS: 기록 필요
- Backend/API/DB: 기록 필요

## 성능 측정

| 항목                | 데이터셋 | Vue median | Vue p95 | 측정일 | 비고 |
| ------------------- | -------: | ---------: | ------: | ------ | ---- |
| 초기 화면           |          |            |         |        |      |
| 탭 전환             |          |            |         |        |      |
| Raw Log 첫 렌더     |          |            |         |        |      |
| 10만 행 스크롤      |          |            |         |        |      |
| 차트 초기 렌더      |          |            |         |        |      |
| Data/Zoom 대체 조작 |          |            |         |        |      |

Phase 0 측정 전에는 React 성능 목표값을 확정하지 않는다.
