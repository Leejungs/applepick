# Frontend

Vite + React 18 + React Router 7 + TanStack Query 5 + MUI + styled-components

```bash
npm install
npm run dev        # http://localhost:3000 , /api 는 API_SERVER(기본 http://localhost:50000)로 프록시
npm run build      # build/ 에 정적 파일 생성 (Dockerfile.web 에서 사용)
```

도커로 띄운 백엔드에 붙이려면: `API_SERVER=http://localhost:2000 npm run dev`

상품 목록은 하드코딩하지 않고 `GET /api/search/products` (백엔드 `backend/catalog.py`) 에서 받아옵니다.
