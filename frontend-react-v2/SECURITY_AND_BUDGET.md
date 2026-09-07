# Phase 1 보안·번들 게이트

## 환경변수

- 브라우저에 노출되는 값은 `VITE_` prefix의 공개 설정만 허용한다.
- 비밀번호, 토큰, DB 접속정보는 저장하지 않는다.
- `.env`는 Git에 추가하지 않는다.

## API/로그

- API client는 request id만 전송하고 인증값·Raw Log를 콘솔에 기록하지 않는다.
- 401은 세션 만료 이벤트로 변환하고 403은 권한 오류로 표시한다.
- 오류 수집에는 사용자 입력·토큰·원본 로그를 포함하지 않는다.

## 번들 기준

- 초기 JS gzip 150KB 이하를 1차 경고 기준으로 둔다.
- 초기 CSS gzip 30KB 이하를 1차 경고 기준으로 둔다.
- AG Grid/ECharts는 실제 도입 Phase에서 route-level lazy loading을 적용한다.
- 기준 초과 시 bundle analyzer로 원인을 기록한 뒤 병합한다.

현재 Phase 1 측정: JS 약 92.5KB gzip, CSS 약 6.2KB gzip.

## 공급망

- lockfile 변경 시 `npm audit --omit=dev`와 라이선스 검사를 수행한다.
- 설치 스크립트는 승인된 패키지만 허용한다.
