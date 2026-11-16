import { execFileSync } from 'node:child_process'
import { BACKEND, PYTHON, entornoDelBackend } from './entorno'

function ejecutarEnElBackend(modulo: string, ...argumentos: string[]) {
  execFileSync(PYTHON, ['-m', modulo, ...argumentos], {
    cwd: BACKEND,
    env: { ...process.env, ...entornoDelBackend() },
    stdio: 'inherit',
  })
}

/** Antes de todas las pruebas: base E2E con el esquema recreado y los datos de demo cargados. */
export default function globalSetup() {
  ejecutarEnElBackend('scripts.reiniciar_bd')
  ejecutarEnElBackend('scripts.cargar_datos_demo', '--reiniciar')
}
