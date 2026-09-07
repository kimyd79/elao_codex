# Phase 1 검증계획

- 새 작업 디렉터리에서 `npm ci` 후 dev/build/preview가 성공하는지 확인한다.
- TypeScript 오류 0건, lint 오류 0건, 단위 테스트 통과를 확인한다.
- 존재하지 않는 API, timeout, 취소, 401/403/5xx, 빈 응답을 mock으로 검증한다.
- 로그인 전 보호 라우트 차단, 로그인 후 접근, 세션 만료 redirect를 검증한다.
- 모바일 최소 폭과 키보드 Tab 이동, 포커스 표시를 확인한다.
- `npm audit`/license 검사와 번들 크기 budget을 확인한다.
- CSP, source map 공개 범위, 민감정보가 오류/성능 이벤트에 포함되지 않는지 확인한다.

완료 조건: 빈 AppShell이 독립 실행·빌드되고 CI가 동일 검증을 통과한다.
