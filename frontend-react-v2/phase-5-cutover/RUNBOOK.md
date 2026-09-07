# React v2 병행운영 및 전환 Runbook

## 기동

```powershell
cd C:\Codex\ELAO\frontend-react-v2
npm.cmd ci
npm.cmd run dev -- --host 127.0.0.1 --port 5174
```

운영 빌드는 `npm.cmd run build` 결과의 `dist`를 정적 호스트에 배포하고, `/mwla/*` API는 기존 Django reverse proxy로 전달합니다.

## 점검 순서

1. `/login` 로그인 게이트 확인
2. `/initialization` 프로젝트·포맷·파일 업로드 확인
3. `/lookup` cursor 조회와 상세 이동 확인
4. `/analysis` 및 `/comparison_chart` 서버 집계 응답과 DataZoom 확인
5. `/project`, `/logformat`, `/metrics` 관리 목록 및 생성 API 확인
6. 기존 Vue 진입점과 React 진입점을 각각 확인한 뒤 feature flag를 전환

## 롤백

- React 정적 호스트의 feature flag를 Vue 진입점으로 되돌립니다.
- API/DB 스키마는 변경하지 않으므로 애플리케이션 롤백만 수행합니다.
- 전환 전 백업은 `C:\Codex\ELAO\backups` 아래 timestamp 폴더를 사용합니다.

## 검증 명령

```powershell
npm.cmd run format:check
npm.cmd run typecheck
npm.cmd run lint
npm.cmd test -- --run
npm.cmd run e2e
npm.cmd run build
```

## Windows `npm ci` 잠금 복구

`@rollup/rollup-win32-x64-msvc` 또는 `@esbuild/win32-x64`의 `.node`/`.exe` 파일에서 `EPERM unlink`가 발생하면 개발 서버와 테스트 프로세스를 종료하고 재부팅 후 다음 순서로 실행합니다.

```powershell
cd C:\Codex\ELAO\frontend-react-v2
npm.cmd ci
```

잠금이 계속되면 `npm.cmd install`로 의존성을 복구한 뒤 `typecheck`, `lint`, `test`, `build`를 재실행합니다. 잠금 파일을 강제 삭제하지 않습니다.
