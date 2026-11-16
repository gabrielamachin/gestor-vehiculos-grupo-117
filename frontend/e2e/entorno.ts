import path from 'node:path'

/** Las pruebas se ejecutan desde frontend/ (npm run test:e2e): el backend es la carpeta hermana. */
export const BACKEND = path.resolve(process.cwd(), '..', 'backend')

/** Python del entorno virtual del backend (no hace falta activarlo). Se puede forzar con E2E_PYTHON. */
export const PYTHON =
  process.env.E2E_PYTHON ??
  path.join(BACKEND, '.venv', ...(process.platform === 'win32' ? ['Scripts', 'python.exe'] : ['bin', 'python']))

/** Variables con las que corre el backend durante las pruebas: apunta SIEMPRE a la base E2E, nunca a la de desarrollo. */
export function entornoDelBackend(): Record<string, string> {
  const baseDeDatos = process.env.E2E_DATABASE_URL
  if (!baseDeDatos) {
    throw new Error(
      'Falta la variable E2E_DATABASE_URL. Ejemplo (PowerShell):\n' +
        '  $env:E2E_DATABASE_URL="postgresql://postgres:TU_CLAVE@localhost:5432/gestor_vehiculos_e2e"\n' +
        'La base debe existir y su nombre debe contener "e2e" o "test": cada corrida BORRA y recrea sus tablas.',
    )
  }
  return {
    DATABASE_URL: baseDeDatos,
    JWT_SECRET: 'secreto-e2e-con-mas-de-32-caracteres-xxxxxxxx',
    COOKIE_SECURE: 'false',
  }
}
