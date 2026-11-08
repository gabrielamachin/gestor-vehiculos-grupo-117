import type { Tono } from '../../shared/componentes/TarjetaIndicador'
import { TarjetaIndicador } from '../../shared/componentes/TarjetaIndicador'
import type { Orientacion } from './tipos'

const TITULOS: Record<Orientacion['estado'], { titulo: string; tono: Tono }> = {
  sin_datos: { titulo: 'Sin datos suficientes', tono: 'neutro' },
  reparar: { titulo: 'Seguir reparando parece razonable', tono: 'ok' },
  evaluar: { titulo: 'Conviene vigilar la evolución', tono: 'alerta' },
  considerar_reemplazo: { titulo: 'Considerá evaluar un reemplazo', tono: 'peligro' },
}

export function OrientacionTarjeta({ datos }: { datos: Orientacion }) {
  const { titulo, tono } = TITULOS[datos.estado]

  return (
    <TarjetaIndicador titulo="¿Reparar o reemplazar?" tono={tono}>
      <p className="text-lg font-semibold text-slate-900">{titulo}</p>
      <p className="mt-1 text-sm text-slate-700">{datos.mensaje}</p>

      {datos.senales.length > 0 && (
        <ul className="mt-3 space-y-1.5">
          {datos.senales.map((senal) => (
            <li key={senal.codigo} className="flex gap-2 text-sm text-slate-700">
              <span aria-hidden="true" className={senal.cumplida ? 'text-red-600' : 'text-emerald-600'}>
                {senal.cumplida ? '●' : '○'}
              </span>
              <span>
                <span className="sr-only">{senal.cumplida ? 'Se cumple: ' : 'No se cumple: '}</span>
                {senal.descripcion}
              </span>
            </li>
          ))}
        </ul>
      )}

      <p className="mt-3 text-xs text-slate-500">{datos.aviso}</p>
    </TarjetaIndicador>
  )
}
