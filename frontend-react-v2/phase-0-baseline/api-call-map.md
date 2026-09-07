# 프런트 API 호출 매핑

출처: `rg` 정적 추출. 정확한 request/response 필드는 Network fixture로 보완한다.

| 영역      | 주요 호출                                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 인증      | `POST /rest-auth/login/`, `GET /rest-auth/user/`, `POST /rest-auth/logout/`, `POST /rest-auth/registration/`                                                       |
| 초기화    | `POST /logmaster/`, `POST /logmaster/create_dynamic_logdetail/`, `POST /logfile/`, `POST /logdetail_dynamic/`, `GET /logfile`, `GET /logdetail_dynamic/start_end/` |
| Lookup    | `GET /logfile`, `GET /logdetail_dynamic/`, `POST /logdetail_dynamic/get_before_after_detail/`                                                                      |
| 분석      | `POST /logdetail_dynamic/statistics/`, `POST /logdetail_dynamic/chartdata/`, `POST /logdetail_dynamic/findings/`, `POST /logdetail_dynamic/uridetail/`             |
| 비교      | `POST /logdetail_dynamic/chartdata_diff/`, findings/statistics 공통 action                                                                                         |
| 프로젝트  | `GET/POST/PUT/DELETE /logmaster/`, `POST /logmaster/delete_dynamic_logdetail/`                                                                                     |
| 로그 포맷 | `GET/POST/PUT/DELETE /logformat/`, `POST /logformat/assist/`, `GET /logformatstring/formatkind_list/`                                                              |
| 메트릭    | `GET/POST/PUT/DELETE /metrics/`, `GET/POST/PUT/DELETE /logmastermetric/`                                                                                           |

React API client는 이 호출을 feature별 함수로 감싸고, 컴포넌트가 URL 문자열이나 query encoding을 직접 조립하지 않도록 한다.
