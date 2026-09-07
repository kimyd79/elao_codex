# 운영 보안 헤더 초안

reverse proxy 또는 정적 호스팅에서 다음 헤더를 적용한다.

- `Content-Security-Policy`: 허용 script/style/connect origin을 명시
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy`: 사용하지 않는 기능 차단
- HTTPS 환경의 `Strict-Transport-Security`

CSP의 API connect-src에는 운영 Django API origin만 허용하고, 개발 환경 origin은 별도 설정으로 둔다.
