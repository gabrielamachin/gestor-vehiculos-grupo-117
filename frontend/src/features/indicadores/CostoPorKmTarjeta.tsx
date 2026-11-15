import type { ReactNode } from 'react'
import { formatoKm, formatoMoneda } from '../../shared/formato'
import { TarjetaIndicador } from '../../shared/componentes/TarjetaIndicador'
import type { CostoPorKm } from './tipos'

export function CostoPorKmTarjeta({ datos }: { datos: CostoPorKm }) {
  let contenido: ReactNode

  if (datos.estado === 'ok' && datos.costo_por_km !== null && datos.km_recorridos !== null) {
    contenido = (
      <>
        <p className="text-3xl font-semibold text-slate-900">
          {formatoMoneda(datos.costo_por_km, 2)}
          <span className="text-base font-normal text-slate-500"> por km</span>
        </p>
        <dl className="mt-4 grid grid-cols-2 gap-3 border-t border-slate-200 pt-3 text-sm">
          <div>
            <dt className="text-xs text-slate-500">Gasto acumulado</dt>
            <dd className="mt-1 font-medium text-slate-700">{formatoMoneda(datos.total_gastado)}</dd>
          </div>
          <div>
            <dt className="text-xs text-slate-500">Distancia recorrida</dt>
            <dd className="mt-1 font-medium text-slate-700">{formatoKm(datos.km_recorridos)}</dd>
          </div>
        </dl>
      </>
    )
  } else if (datos.estado === 'sin_lecturas') {
    contenido = <p className="text-sm text-slate-500">Cargá una lectura de kilometraje para calcular cuánto te cuesta cada kilómetro.</p>
  } else {
    contenido = <p className="text-sm text-slate-500">Todavía no recorriste kilómetros desde el kilometraje inicial.</p>
  }

  return <TarjetaIndicador titulo="Costo real por kilómetro">{contenido}</TarjetaIndicador>
}
