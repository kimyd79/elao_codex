# Phase 1 작업방법

- 기존 Vue package를 복사하지 않고 React 전용 lockfile을 새로 생성한다.
- API client는 feature 코드에서 직접 fetch/axios를 호출하지 못하도록 모듈 경계를 둔다.
- shadcn/ui 원본 컴포넌트와 업무용 래퍼를 분리한다.
- 환경변수는 `.env.example`과 런타임 검증 스키마를 함께 관리한다.
- CI는 install → lint → typecheck → unit → build 순서로 실행한다.
- lockfile을 변경할 때는 dependency diff, license, 취약점 결과를 함께 보관한다.
- API client는 공통 correlation id를 전송하고 민감한 request/response를 로깅하지 않는다.
- bundle analyzer를 기준 빌드에 연결해 큰 의존성 증가를 차단한다.
