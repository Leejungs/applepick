import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  // 개발 서버에서 /api 요청을 넘길 백엔드 주소
  // - 로컬 Flask(python run.py): http://localhost:50000 (기본값)
  // - docker compose 로 띄운 경우: http://localhost:2000
  const apiTarget = env.API_SERVER || 'http://localhost:50000';

  return {
    plugins: [react()],
    server: {
      port: 3000,
      strictPort: true, // 3000 이 사용 중이면 다른 포트로 몰래 뜨지 않고 에러
      proxy: {
        '/api': { target: apiTarget, changeOrigin: true },
        '/docs': { target: apiTarget, changeOrigin: true },
      },
    },
    build: {
      outDir: 'build',
      rollupOptions: {
        output: {
          manualChunks: {
            react: ['react', 'react-dom', 'react-router-dom'],
            mui: ['@mui/material', '@mui/icons-material'],
            chart: ['chart.js', 'react-chartjs-2'],
          },
        },
      },
    },
  };
});
