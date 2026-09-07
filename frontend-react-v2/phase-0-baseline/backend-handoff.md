# 백엔드 인계 목록

Phase 0 조사에서 프런트 구현 전에 백엔드와 확정할 항목이다.

| 우선순위 | 항목         | 필요한 결정                                  | 완료 증거           |
| -------- | ------------ | -------------------------------------------- | ------------------- |
| P0       | 인증         | 세션/토큰, CSRF, 401/403, 만료               | OpenAPI/계약 테스트 |
| P0       | Raw Log 조회 | cursor, 안정 정렬, snapshot/consistency      | API fixture         |
| P0       | 집계         | interval, timezone, 빈 구간, 반올림          | 수치 fixture        |
| P0       | 업로드 작업  | job ID, progress, cancel, retry, idempotency | 상태 전이 테스트    |
| P1       | 상세 문맥    | before/after 라인, 권한, 마스킹              | 응답 샘플           |
| P1       | 다운로드     | 비동기 생성, 파일명, CSV escape, 권한        | 보안 테스트         |
| P1       | 오류         | 공통 code/message/field errors               | 오류 fixture        |
| P1       | 호환성       | 기존 Vue API 유지 기간과 v2 API 버전         | 배포 계획           |

추가 확인: 현재 프런트는 `limit`/`offset` 목록과 다수의 POST action을 사용한다. cursor 기반 React API를 도입할 경우 기존 endpoint를 깨지 않는 `/v2/` 계약 또는 호환 adapter가 필요하다.

프런트는 이 목록이 확정되기 전 새 endpoint를 임의로 구현하지 않는다.

## 기존 로그에서 확인된 안정성 이슈

`EALO/backend/logs/mwla.log`에서 `statistics`, `chartdata`, `findings`가 `NoneType` iterable 및 `totalCnt` 미할당으로 오류를 기록한 사례가 있다. 이 오류는 React 문제가 아니므로 Phase 0에서 백엔드 재현·수정 또는 명시적 오류 계약으로 분리한다.
