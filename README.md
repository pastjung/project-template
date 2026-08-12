# React Vite App Template

React 19 + TypeScript(strict) + Vite 7 스타터입니다. ESLint(flat config),
Prettier, Vitest(+Testing Library), Docker(nginx) 빌드를 포함합니다.

## 기술 스택

- React 19, TypeScript (strict)
- Vite 7 (`@` → `src` alias, `/api` 프록시 예시 포함)
- ESLint 9 flat config + typescript-eslint + react-hooks/react-refresh
- Prettier
- Vitest + Testing Library (jsdom)

## Run Locally

```bash
npm ci
npm run dev
```

`.env.example`을 복사해 `.env`를 만들면 `VITE_API_BASE_URL`이 적용됩니다.
env 변수 타입은 `src/vite-env.d.ts`에서 관리합니다.

## Scripts

| Script | 설명 |
| --- | --- |
| `npm run dev` | 개발 서버 |
| `npm run build` | 타입 체크(tsc -b) 후 프로덕션 빌드 |
| `npm run preview` | 빌드 결과 로컬 확인 |
| `npm run lint` | ESLint 검사 |
| `npm run format` / `format:check` | Prettier 포맷 / 검사 |
| `npm run typecheck` | TypeScript 타입 체크 |
| `npm run test` | Vitest 단위 테스트 |

## Backend Proxy

`vite.config.ts`의 `server.proxy`가 `/api` 요청을 `http://localhost:8000`으로
전달합니다. 백엔드 주소에 맞게 조정하세요.

## Docker

```bash
docker build -t react-vite-app .
docker run --rm -p 8080:80 react-vite-app
```
