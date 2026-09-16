# ELAO AI Findings 단계별 구현 계획

## 상태와 범위

- 1단계: 완료 — 소스 연결 지점 확인, 설계 및 단계별 검증 기준 작성.
- 2단계: 핵심 데이터 구성 서비스 및 오프라인 검증 구현. 아래 잔여 검증 항목 때문에 전체 종료는 보류.
- 3~5단계: 미착수. 실제 API 호출, 외부 로그 전송, 운영 설정 변경 없음.
- OpenAI API 사용. 현재 Search 결과의 집계 요약과 대표 로그를 전달하고 한국어 분석 의견을 표시한다.
- 결과는 화면 메모리에만 보관한다. 분석 이력 테이블, V2 이중 저장, 동적 테이블 변경은 하지 않는다.
- 기본 진입점은 Analysis의 Findings. Comparison 화면 확장은 이번 범위에서 제외한다.
- 기존 규칙 기반 Findings API는 유지하고 AI API를 별도로 추가한다.

## 1단계 — 소스 확인 및 설계

### 확인한 연결 지점

| 파일 | 확인 내용 | 반영할 작업 |
|---|---|---|
| `frontend-react-v2/src/features/analysis/AnalysisWorkspacePage.tsx` | Findings가 `/logdetail_dynamic/findings/`에 `filter: {}` 전송 | 마지막 실행한 Search 조건을 별도 상태로 보관하여 전달 |
| 같은 파일의 Search | `onSearch`와 `elao:analysis-search` 이벤트로 조회조건 전달 | 입력 중인 조건과 적용한 조건을 구분, 초기 자동 검색도 동일 경로 사용 |
| `frontend-react-v2/src/features/analysis/service.ts` | `toAnalysisRequest`가 배열·exclude boolean·project_id 정규화 | AI 요청도 동일 의미의 필터 사용, 별도 타입 정의 |
| `EALO/backend/loganalyzerapi/views.py` | 기존 findings는 LogMasterMetric 기반 규칙 분석 | AI 분석 서비스는 별도 모듈로 분리 |
| 같은 파일의 statistics | type=0은 필터 없이 프로젝트 전체 조회 | 필터 적용 집계에 type=0 결과를 그대로 재사용하지 않음 |
| `EALO/backend/loganalyzer/settings.py` | 기본 IsAuthenticated 설정이 주석 처리되어 있음 | 새 AI API에 명시적 인증·프로젝트 접근권한 적용 |
| `EALO/backend/loganalyzerapi/models.py` | 프로젝트 creator는 문자열 | 인증 사용자와 비교, 클라이언트 creator를 신뢰하지 않음 |

이 단계는 정적 소스 확인이며 DB 데이터 정확성, 운영 인증 정책, API 키 보유 여부까지 검증한 것은 아니다.

### 처리 계약

신규 제안 경로: `POST /mwla/logdetail_dynamic/ai_findings/`.

요청은 `project_id`, `filter`, `request_id`만 받는다. 원문·집계·모델명·API 키를 클라이언트가 지정하지 않는다.
filter는 projectServers, dateFromValue/dateToValue, timeFromValue/timeToValue,
conditionValue, searchValue, excludeSearch, ttFromValue/ttToValue를 포함한다.
중첩 project_id가 있다면 최상위 값과 일치해야 한다.

응답은 다음 영역으로 분리한다.

- scope: 적용 조건, 실제 데이터 범위, 조회 건수, 시간대와 응답시간 단위.
- sampling: 샘플 수, 추출 기준, 잘림 여부, 데이터 누락과 제한 사항.
- analysis: summary, findings(심각도·관측 사실·근거 ID·원인 가설·권고), limitations.
- metadata: request_id, 데이터 추출 시각, 모델, 토큰 사용량. 로그 본문과 결과를 서버 로그에 기록하지 않는다.

AI 출력은 JSON Schema로 검증하며 형식 준수와 내용 정확성은 별개로 취급한다.
근거 ID는 전송한 집계/샘플 ID와 대조하고 존재하지 않는 근거는 표시하지 않는다.

## 2단계 — 분석 데이터 구성 (외부 호출 없음)

### 작업방법

1. 인증, 프로젝트 존재/소유권, 필터 유효성을 검사하는 별도 서비스와 serializer를 만든다.
   초기 정책은 소유자 또는 Django staff/superuser만 허용한다. 공유 프로젝트 정책은 별도 명시 전까지 허용하지 않는다.
2. 기존 동적 테이블 조회 필터를 검토해 공통화하거나 동등한 안전한 필터 함수를 만든다.
   임의 테이블명/SQL을 받지 않고 검증된 프로젝트로 모델을 결정한다.
3. 하나의 조회 범위에서 전체 건수, 상태 분포, 응답시간, 시간대별 요청/오류, URL/IP 상위를 집계한다.
4. 정상·오류·느린 요청·시간대 분산 샘플을 중복 제거하여 최대 200건 추출한다.
   정렬 기준을 고정하고 ORDER BY RANDOM 및 전체 로그의 Python 메모리 적재는 피한다.
5. 초기 제한안: 샘플당 2,000자, 전체 입력 JSON 128 KiB, 시간 버킷 최대 120개, 상위 항목 각 10개.
   제한 초과 시 샘플부터 줄이고 범위·집계는 유지한다. 최종 모델의 토큰 한도도 별도로 검사한다.
6. 응답시간은 파일 포맷별 단위를 확인해 정규화한다. 누락 값은 0으로 바꾸지 않는다.
   로그에 시간대가 없으면 임의로 UTC/KST를 붙이지 않고 unknown으로 명시한다.
7. 데이터 변동 시 집계·샘플 불일치를 막을 읽기 일관성 정책을 정하고 OpenAI 호출 전 DB 트랜잭션을 끝낸다.

### 검증/종료 기준

- 작은 고정 fixture에서 검색조건별 건수·오류율·응답시간을 수작업 기대값과 비교.
- 날짜 경계, 모든/일부/미선택 instance, exclude=false, timetaken=0, 단위 혼합 테스트.
- 미인증/타인 프로젝트/잘못된 필터는 거절. 빈 결과는 외부 호출 대상에서 제외.
- 샘플 중복·범위 이탈 없음, 크기 제한 준수, 외부 HTTP 호출 0회.
- 대용량 fixture로 쿼리 수·소요시간·실행계획 측정. p95 등 추가 집계의 비용은 별도 확인.

## 3단계 — OpenAI 연결 및 백엔드 API

### 2단계 구현/검증 기록

- 구현: `EALO/backend/loganalyzerapi/ai_dataset.py`.
- 독립 검증: `scripts/test_ai_dataset_offline.py` (PYTHONPATH=EALO/backend).
- 날짜/인스턴스/조건/exclude/응답시간 필터, 인증·소유권 검사, 파일별 기존 저장 단위 환산.
- 최대 120개 시계열 구간, 요청/고유 IP 급증·급감, 오류율/평균 응답시간 증가 후보.
- 후보 최대 5개에서 현재·직전 구간의 IP/전체 요청 문자열/IP×요청 변화 추출.
- 대표 로그 중복 제거, 최대 200건 및 128 KiB 제한. 후보 근거와 샘플 ID 포함.
- PostgreSQL 진입점은 repeatable-read/read-only transaction 및 문장별 15초 제한 사용.
- 10개 오프라인 테스트 통과. 합성 100,000행 SQLite 집계: 0.563초, 15쿼리, 40샘플
  (데이터 생성 제외, 단일 로컬 측정이며 PostgreSQL 성능 추정에 사용하지 않음).
- Django `manage.py check` 통과. 운영 로그파일 권한 문제로 동일 명령을 승인된 권한으로 재실행.
- 외부 네트워크 요청 없음, 기존 화면/API 변경 없음, migration 없음.

잔여 항목(3단계 실제 연동 전 검증):

- 운영 PostgreSQL 동적 모델 진입점 통합 검증 완료(아래 후속 기록). 더 큰 데이터/최악 분포의 부하 시험은 별도.
- 전체 데이터 구성 60초 쿼리 시작 예산 적용. 실행 중 SQL은 별도 15초 제한이므로 정확한 60초 hard deadline은 아님.
- 전체 지표와 독립적인 IP/요청 시계열 탐지 구현 완료. 추적 범위는 시간대별 상위 10개 합집합 중 피크 건수 기준 최대 200개/필드.
- URL 경로 정규화 및 정상/오류/이상 구간 샘플 배분 개선. 현재는 전체 요청 문자열 기준.
- 파서별 저장 단위의 통합 fixture 검증, 상위 백분위 응답시간 집계 비용 검토.
- 실제 동적 테이블 wrapper의 DB 통합 테스트 실행 완료. 사용자 권한 거절 경로는 오프라인 테스트로 검증.

### 2단계 후속 검증: 시간대별 entity 변화 및 운영 DB

- IP와 요청 문자열별로 직전 3~5개 완전한 시간구간 중앙값 대비 3배 증가 또는 70% 감소 탐지.
  기준/현재 최대 건수 최소 20 조건 적용. 증가·감소 근거, 과거 건수, 현재 점유율 포함.
- 전체 요청 수와 고유 IP 수가 일정해도 entity 교체를 탐지하고 기존 상세 추출 대상에 포함.
- top-N 누락은 0으로 간주하지 않고 추적 항목의 실제 시간대별 건수를 재집계.
- 범위 제한을 entity_coverage에 명시: 필드별 최대 200개 추적, 변화 후보 최대 100개.
  모든 저빈도 IP/URL을 빠짐없이 검사하는 기능은 아니며 URL 경로 정규화는 여전히 별도 과제.
- 시간대별 집계를 최대 120회 반복 호출하던 방식에서 1회 GROUP BY로 개선.
- PostgreSQL 트랜잭션 내부에서만 JIT 비활성화, 제한된 그룹 조회에 일반 커서 사용.
  운영 DB 전역 설정/테이블/인덱스는 변경하지 않음.
- 오프라인 테스트 13개 통과: 일정 트래픽의 IP/URL 교체, 안정 구간 무탐지,
  top-N 순위 이탈의 오탐 방지 포함. 10만 행 1.328초/10쿼리(SQLite 단일 측정).
- `scripts/verify_ai_dataset_postgres.py`: 서버 기동과 동일한 환경변수 사용,
  read-only repeatable-read 트랜잭션 확인. 최근 데이터가 있는 프로젝트 3개 검증.
- 첫 운영 시도에서 쿼리 예산 초과를 발견하여 집계 반복을 제거한 뒤 3개 모두 통과.
  중간 버전 측정: 300,000행 53.484초, 274,187행 34.844초, 200,000행 37.859초.
- 최종 코드 운영 재검증 3개 모두 통과(단일 실행, 캐시·동시 부하 영향 포함):

  | 행 수 | 소요시간 | SQL 수 | 시간구간 수 | 샘플 수 | 독립 entity 후보 | JSON 크기 |
  |---:|---:|---:|---:|---:|---:|---:|
  | 300,000 | 43.937초 | 105 | 96 | 114 | 100 | 130,735 bytes |
  | 274,187 | 28.672초 | 40 | 120 | 80 | 0 | 56,147 bytes |
  | 200,000 | 31.422초 | 105 | 96 | 167 | 62 | 130,668 bytes |

  아직 수십 초가 걸리므로 화면 연결 단계에서 로딩 상태·중복 클릭 방지·적절한 요청 제한 필요.
- 검증 항목: 별도 필터 조회 건수 = 결과 전체 건수 = 시계열 합계, JSON 128 KiB 이내.
  EXPLAIN(ANALYZE 미사용)에서 기본 조회 Seq Scan 확인. 원문/IP/URL 결과는 콘솔에 출력하지 않음.
- 외부 LLM 호출 및 전송 없음. API/화면 연결 없음.

재검증 명령(저장된 비밀번호를 출력하지 않음):

```powershell
cd C:\Codex\ELAO\EALO\backend
. C:\Codex\ELAO\scripts\windows-common.ps1
Import-EaloEnvironment
$env:PYTHONPATH = 'C:\Codex\ELAO\EALO\backend'
& C:\Codex\ELAO\.venv312\Scripts\python.exe C:\Codex\ELAO\scripts\verify_ai_dataset_postgres.py
```

### 작업방법

- 공식 Python SDK와 Responses API를 별도 provider로 구현하고 테스트에서는 fake provider 주입.
- 서버 설정: AI_FINDINGS_ENABLED(기본 false), OPENAI_API_KEY, OPENAI_MODEL,
  입력/출력 한도, 요청 timeout. 키는 서버 환경에만 두고 프런트·응답·Git에 노출하지 않는다.
- 모델은 접근 가능한 Structured Outputs 지원 모델 중 평가 후 지정한다. 지금 모델명·가격은 확정하지 않는다.
- `store: false`, tools 미제공, 로그를 신뢰하지 않는 데이터로 구분. 로그 속 지시를 실행하지 않는다.
- 관측 사실/가설/권고 분리, 근거 없는 장애 원인 단정 금지, 샘플 편향과 비교 기준 부재 명시.
- 인증 이후 사용자별 호출 제한과 중복 요청 제어. 다중 worker에서도 유효한 공유 캐시를 사용하되
  원문·분석 결과는 캐시에 저장하지 않고 짧은 TTL의 요청 잠금만 사용한다.
- timeout/429/인증 실패/모델 거절/불완전 출력/스키마 오류를 안전한 앱 오류로 변환한다.
  SDK 자동 재시도 정책을 명시하여 비용이 중복 발생하는 재시도를 제한한다.
- 초기에는 일반 요청 + 프런트 비동기 대기로 구현. worker 점유 시간을 제한한다.
  처리량 측정 후 작업 큐 도입을 별도 판단하며 가짜 퍼센트 진행률을 만들지 않는다.

### 검증/종료 기준

- mock으로 성공·거절·시간초과·429·잘못된 JSON·빈 결과·미설정 상태 테스트.
- 외부 호출 전 권한/크기 검증, 빈 결과와 기능 비활성 상태는 과금 호출 0회.
- 로그·에러 응답·프런트 번들에 API 키와 원문이 유출되지 않음.
- 실제 호출은 5단계에서 수행. DB migration 없음.

## 4단계 — Findings 화면 연결

### 작업방법

- 부모 화면에서 마지막 Search 적용 조건을 관리해 Findings에 전달한다.
- 조건 편집만으로 호출하지 않는다. Load Findings 클릭 시에만 AI 요청한다.
- 신규 Search/프로젝트 변경 시 기존 결과를 무효화하고 이전 응답의 뒤늦은 덮어쓰기를 방지한다.
- 요청 중 버튼 비활성화와 분석 중 표시, 명시적 재시도, 빈 결과/설정 누락/오류 안내 제공.
- 요약·특이사항·근거·가설·점검사항·한계를 카드 형태로 렌더링. 모델 출력은 HTML로 직접 삽입하지 않는다.
- 전송 범위와 원본 로그 샘플의 외부 전송 사실을 화면에 표시한다.
- AI 비활성 시 기존 규칙 기반 Findings를 유지하고 결과 출처를 구별한다.
- 결과는 컴포넌트 메모리에만 보관. localStorage, DB 분석 이력 저장 없음.

### 검증/종료 기준

- Search 전/후, 입력만 변경, 초기 자동 조회, 프로젝트 전환, 빠른 연속 검색의 상태 테스트.
- 클릭 1회에 AI 요청 1회, 로딩/실패/재시도/장문 결과/XSS 문자열 테스트.
- 기존 Charts·Statistics·Detail·Comparison의 검색 동작 회귀 테스트.
- typecheck, lint, 관련 unit test 및 브라우저 육안 확인.

## 5단계 — 실제 연결 및 운영 검증

- 서버 API 키·모델·사용 한도를 설정한다. 키 값은 대화에 붙여 넣지 않는다.
- 우선 합성 로그로 1회 호출, 이후 허용된 실제 프로젝트의 제한된 범위로 검증한다.
- 집계 수치·근거 행 일치, 한국어 결과의 실용성, 지연, 토큰 사용량과 비용을 기록한다.
- ELAO 결과 미저장과 OpenAI 보관 정책은 별개다. store=false는 모든 보관의 제거를 의미하지 않는다.
- 모델 호출 실패에도 기존 분석 화면이 정상 동작하고 기능 플래그만으로 되돌릴 수 있는지 확인한다.
- 검증 결과에 실행한 항목/미실행 항목을 구분 기록한 뒤 완료 처리한다.

## 공식 참고 문서

- [API 및 서버 환경변수 설정](https://developers.openai.com/api/docs/quickstart)
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [데이터 보관 정책](https://developers.openai.com/api/docs/guides/your-data)

OpenAI Docs 검토를 반영해 구조화 출력 검증, 거절/불완전 응답 처리, 서버 전용 키,
외부 서비스 보관 정책을 구현·검증 항목에 포함했다.
