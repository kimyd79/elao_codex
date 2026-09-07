# 기존 라우트 기준선

출처: `EALO/frontend/src/router.js`

| 경로                    | 이름                 | 화면/역할                 | 가드·전환                                   | React Phase |
| ----------------------- | -------------------- | ------------------------- | ------------------------------------------- | ----------- |
| `/`                     | home                 | 로그인 상태에 따른 진입   | 미로그인 `/login`, 로그인 `/initialization` | 2           |
| `/initialization`       | initialization       | 프로젝트·로그 초기화 단계 | 로그인 필요                                 | 2           |
| `/analysis`             | analysis             | 단일 로그 분석 차트       | 로그인 필요                                 | 4           |
| `/detail`               | detail               | 상세/원본 로그            | 로그인 필요                                 | 3           |
| `/comparison_chart`     | comparison_chart     | 로그 비교 차트            | 로그인 필요                                 | 4           |
| `/comparison_statistic` | comparison_statistic | 비교 통계                 | 로그인 필요                                 | 4           |
| `/lookup`               | lookup               | Raw Log 검색              | 로그인 필요                                 | 3           |
| `/management`           | Management           | 관리 레이아웃             | 로그인 필요                                 | 3           |
| `/logformat`            | logformat            | 로그 포맷 관리            | 로그인 필요, 관리자 정책 확인               | 3           |
| `/register`             | register             | 사용자 등록               | 공개 진입 예외                              | 2           |
| `/login`                | login                | 로그인                    | 이미 로그인 시 initialization 이동          | 2           |
| `/logout`               | logout               | 로그아웃                  | 로그인 필요                                 | 2           |
| `/project`              | project              | 프로젝트 관리             | 로그인 필요, 관리자 정책 확인               | 3           |
| `/metrics`              | metrics              | 메트릭 관리               | 로그인 필요, 관리자 정책 확인               | 3           |
| `/test`                 | fileupload           | 개발용 업로드 테스트      | 제품 전환 제외/보류                         | 0           |

주의: Vue Router의 `children`에 `/logformat`처럼 선행 `/`가 붙어 있어 실제 중첩 레이아웃 동작을 React에서 재검증한다.
