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
        <p className="mt-1 text-sm text-slate-600">
          Gastaste {formatoMoneda(datos.total_gastado)} en {formatoKm(datos.km_recorridos)} recorridos.
        </p>
      </>
    )
  } else if (datos.estado === 'sin_lecturas') {
    contenido = <p className="text-sm text-slate-500">Cargá una lectura de kilometraje para calcular cuánto te cuesta cada kilómetro.</p>
  } else {
    contenido = <p className="text-sm text-slate-500">Todavía no recorriste kilómetros desde el kilometraje inicial.</p>
  }

  return <TarjetaIndicador titulo="Costo real por kilómetro">{contenido}</TarjetaIndicador>
}
