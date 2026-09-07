# Phase 5 작업방법

- CI에서 unit/typecheck/build, 별도 환경에서 E2E/smoke를 실행한다.
- feature flag를 사용자·라우트 단위로 단계적으로 확대한다.
- 전환 전후에 동일 fixture와 동일 API 버전으로 결과를 비교한다.
- 오류율·응답시간 임계치를 초과하면 자동 확대를 중단하고 Vue로 롤백한다.
- 안정화 기간과 삭제 승인 없이 기존 Vue/Lego를 제거하지 않는다.
- 전환 단계별 exit criteria와 rollback criteria를 수치로 문서화한다.
- 구 API/구 프런트 제거는 사용량 0 확인, 백업, 승인, 복구 리허설 순서로 수행한다.
