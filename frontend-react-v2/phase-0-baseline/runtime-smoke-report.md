# Phase 0 런타임 smoke 결과

실행일: 2026-08-14

## 결과

- Vue 개발 서버: `http://127.0.0.1:8080/` 응답 200
- Django API root: `http://127.0.0.1:8000/mwla/` 응답 200
- 실행 자동화: `tools/run-runtime-check.ps1`
- 실행 후 프로세스 정리: 완료

## 재검증 결과

PostgreSQL 서비스가 5432 포트에서 청취한 뒤 재실행한 smoke에서 `/mwla/logmaster/`와 `/mwla/logfile/`를 포함한 DB 의존 endpoint가 HTTP 200을 반환했다. 상세 응답 시간·바이트는 `tools/runtime-check.json`에 기록했다.

## 제한 사항

초기 실행에서는 백엔드의 데이터베이스가 필요한 endpoint를 호출하는 과정에서 PostgreSQL 연결 오류가 확인되었으나, PostgreSQL 청취 상태 복구 후 재검증에 성공했다.

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb8 in position 63
```

이는 React 전환 코드의 오류가 아니라 현재 `.env`의 DB 연결 자격증명/인코딩 또는 PostgreSQL 응답 인코딩을 먼저 정리해야 하는 운영 환경 문제다. 비밀번호 등 민감값은 이 문서에 기록하지 않았다.

## 후속 조치

1. `.env`의 PostgreSQL 연결 설정을 UTF-8 안전한 값으로 확인한다.
2. `/logmaster/`, `/logfile/`, `/logdetail_dynamic/`를 인증·DB 연결 상태에서 재검증한다.
3. 정상 API fixture와 성능 측정값을 `baseline-report.md`에 채운다.
