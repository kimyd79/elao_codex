# Phase 1 작업계획 — React 실행 기반

## 목표

독립 실행 가능한 React + TypeScript + Vite 기반과 공통 실행 규칙을 만든다.

## 작업

1. Node/npm, Vite, TypeScript, 환경변수 스키마를 고정한다.
2. ESLint, Prettier, Vitest, Playwright, typecheck를 구성한다.
3. Tailwind/shadcn/ui와 dense 디자인 토큰을 정의한다.
4. AppShell, ErrorBoundary, Loading/Empty/Error 상태를 만든다.
5. API client에 인증, timeout, AbortSignal, 오류 정규화를 구현한다.
6. React Router, 인증 provider, 권한 가드, 세션 만료 redirect를 만든다.
7. CI에서 lint/typecheck/unit/build를 실행한다.
8. dependency license/audit, bundle size budget, source map 및 CSP 정책을 정한다.
9. 사용자 오류·성능 이벤트를 수집할 observability 인터페이스를 정의한다.

## 산출물

- `package.json`, `vite.config.ts`, `tsconfig.json`
- `src/app`, `src/components`, `src/lib`
- 환경변수 문서와 CI 설정
- dependency/license/audit 보고서와 bundle budget
- 오류·성능 이벤트 타입 및 수집 어댑터
