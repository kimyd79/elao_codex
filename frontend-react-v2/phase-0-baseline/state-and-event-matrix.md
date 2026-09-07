# 상태·이벤트 기준선

출처: `EALO/frontend/src/vuex/store.js`, `actions.js`, `getters.js`, `EventBus.js` 및 컴포넌트 사용 검색.

| 도메인       | 기존 상태                                                                                                                 | React 소유 후보                         | 비고                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | -------------------------------- |
| 프로젝트     | `projectName`, `projectDescription`, `projectID`, `projectFiles`                                                          | init/management query cache             | 저장 후 ID 전파 필요             |
| 로그         | `fileNames`, `logFormat`, `logFileID`, `projectServers`, `projectServers2`                                                | init + selected-log context             | 비교 1/2 분리 유지               |
| 전역 시간/축 | `global_*Date`, `global_*Time`, `global_Y_*`                                                                              | analysis/comparison URL + feature store | 시간대·해상도 계약 필요          |
| 검색 1       | `fromDate`, `toDate`, `fromTime`, `toTime`, `fromTimeTaken`, `toTimeTaken`, `condition`, `searchKeyword`, `excludeSearch` | lookup/analysis filter                  | API query 직렬화 필요            |
| 검색 2       | `fromDate2`, `toDate2`, `fromTime2`, `toTime2`, `condition2`, `searchKeyword2`, `excludeSearch2`                          | comparison filter                       | 첫 검색과 독립 보존              |
| 상세         | `detailcondition`, `detailsearchKeyword`, `threshold`                                                                     | detail query                            | 통계 클릭에서 전달               |
| UI 토글      | `toggleSearch`, `toggleSearch1`, `toggleSearch2`                                                                          | feature local UI state                  | URL 저장 여부 결정               |
| 인증         | `userToken`, `userName`                                                                                                   | auth provider/session                   | 저장 위치·만료 정책 확정         |
| 팝업         | `popupHeader`, `popupBody`, `popupButton`, `popupReturn`, `popupKind`, `popupFormatId`, `popupFormatKind`                 | overlay state                           | EventBus와 중복 여부 조사        |
| 메뉴/메트릭  | `currentMenu`, `metricId`                                                                                                 | app navigation + metric context         | 현재 getter 대소문자 불일치 점검 |

## 기준선 이슈

- `store.js`에는 `popupDate`, `detailcondition2`, `detailsearchKeyword2`가 동적으로 추가되는 경로가 있어 React 타입에서 명시해야 한다.
- `getters.js`의 `getMetricId`/`getCurrentMenu`가 state의 `metricId`/`currentMenu`와 대소문자가 다르므로 실제 사용 결과를 fixture로 확인한다.
- `SET_GLOBAL_Y_REQUEST_SBAR` 등 일부 mutation이 의도한 필드가 아닌 다른 필드를 갱신하는지 이전 전에 확인한다.
- `vuex-persistedstate`가 저장하는 인증·검색 상태를 React에서 그대로 저장하지 말고 보안 정책을 먼저 확정한다.
