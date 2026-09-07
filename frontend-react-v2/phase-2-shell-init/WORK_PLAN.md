# Phase 2 작업계획 — AppShell·인증·탭·초기화

## 목표

기존 메뉴·인증 흐름과 `Init.vue`의 단계형 탭을 React에서 동일하게 동작시킨다.

## 작업

1. `/`, `/login`, `/logout`, `/register`, `/initialization`을 구성한다.
2. 상단 메뉴·사이드 메뉴·현재 메뉴·권한별 메뉴를 이전한다.
3. `tabs[].isSelected`를 `project/server/logformat/range` 단계 상태로 변환한다.
4. 이전/다음/삭제/새 프로젝트와 조건부 단계 표시를 이전한다.
5. 프로젝트·서버·인스턴스·로그 포맷 선택을 typed form으로 구현한다.
6. 업로드 진행률·취소·재시도·중복 제출 방지를 구현한다.
7. 탭 상태를 URL route/query와 동기화한다.
8. 저장·삭제·업로드 요청의 idempotency와 중복 제출 방지를 API 계약에 반영한다.
9. 서버 검증 오류, 네트워크 재시도, 이탈 시 미완료 작업 복구 정책을 구현한다.

## 산출물

- `src/features/init`
- 인증/권한 가드
- 탭 상태 전이 테스트
- 초기화 API adapter와 fixture
- 인증·업로드 상태 전이표와 idempotency 테스트
