# Phase 3 작업계획 — 관리·Lookup·Detail·AG Grid

## 목표

관리 화면과 원본 로그 조회를 서버 커서·AG Grid 가상화로 이전한다.

## 작업

1. `/project`, `/logformat`, `/metrics`를 이전한다.
2. Lookup 검색어·제외어·전후 라인·날짜·서버 조건을 typed filter로 정의한다.
3. AG Grid adapter에 컬럼·정렬·선택·상세·다운로드를 연결한다.
4. cursor pagination, 안정 정렬, 필터 변경 시 cursor 초기화, 중복 행 방지를 구현한다.
5. Detail에서 선택 행의 원본·전후 문맥을 지연 조회한다.
6. 10만·100만·수백만 건 데이터셋으로 가상화와 메모리를 측정한다.
7. 행 고유 키, 정렬 안정성, 데이터 변경 중 cursor 일관성 정책을 확정한다.
8. Raw Log 마스킹, 다운로드 권한, 파일명/CSV injection 방지 규칙을 적용한다.

## 산출물

- `src/features/management`, `lookup`, `detail`
- AG Grid column/row adapter
- cursor API contract test
- 대용량 성능 보고서
- 데이터 일관성·보안 다운로드 테스트
