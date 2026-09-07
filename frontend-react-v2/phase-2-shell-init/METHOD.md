# Phase 2 작업방법

- UI 탭과 업무 단계 상태를 분리하고 단계 전이는 순수 reducer/state machine으로 작성한다.
- 기존 API 요청은 Phase 0 계약 adapter를 통해 호출한다.
- 폼은 schema validation과 서버 오류를 필드 단위로 매핑한다.
- 탭별 상태는 URL에는 식별자만, 검색·폼 상태는 feature store에 저장한다.
- 업로드는 작업 ID 기반 polling 또는 progress 이벤트로 추적한다.
- 저장·삭제·업로드 버튼은 pending 동안 잠그고 idempotency key를 사용한다.
- 인증 쿠키/CSRF 또는 토큰 방식은 백엔드 확정 계약 하나만 사용하며 혼용하지 않는다.
- 권한은 메뉴 숨김만으로 처리하지 않고 API 401/403 응답도 화면에서 처리한다.
