import { defineConfig, devices } from '@playwright/test'
import { BACKEND, PYTHON, entornoDelBackend } from './e2e/entorno'

/**
 * Pruebas end-to-end: levantan la API (contra la base E2E) y el frontend, y manejan un navegador real.
 * Ver e2e/README.md. Se ejecutan con `npm run test:e2e` desde frontend/.
 *
 * `reuseExistingServer: false` es deliberado: si ya hay una API o un frontend de desarrollo corriendo en esos
 * puertos, las pruebas se niegan a arrancar en lugar de reutilizarlos (la API de desarrollo apunta a tu base real).
 */
export default defineConfig({
  testDir: './e2e',
  globalSetup: './e2e/global-setup.ts',
  timeout: 30_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: 'http://localhost:5173',
    locale: 'es-AR',
    timezoneId: 'America/Argentina/Buenos_Aires',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    {
      command: `"${PYTHON}" -m uvicorn app.main:app --port 8000`,
      cwd: BACKEND,
      env: entornoDelBackend(),
      url: 'http://localhost:8000/health',
      reuseExistingServer: false,
      timeout: 60_000,
      stdout: 'pipe',
      stderr: 'pipe',
    },
    {
      // --strictPort: falla en lugar de buscar otro puerto (el proxy y baseURL esperan el 5173)
      command: 'npm run dev -- --port 5173 --strictPort',
      url: 'http://localhost:5173',
      reuseExistingServer: false,
      timeout: 60_000,
      stdout: 'pipe',
      stderr: 'pipe',
    },
  ],
})
