import { formatoMoneda, formatoPorcentaje } from '../../shared/formato'
import { TarjetaIndicador } from '../../shared/componentes/TarjetaIndicador'
import type { GastoPorCategoria } from './tipos'

export function GastoPorCategoriaTarjeta({ datos }: { datos: GastoPorCategoria }) {
  if (datos.categorias.length === 0) {
    return (
      <TarjetaIndicador titulo="Gasto por categoría (últimos 12 meses)">
        <p className="text-sm text-slate-500">Todavía no hay gastos en los últimos 12 meses.</p>
      </TarjetaIndicador>
    )
  }

  return (
    <TarjetaIndicador titulo="Gasto por categoría (últimos 12 meses)">
      <p className="mb-4 text-2xl font-semibold text-slate-900">{formatoMoneda(datos.total)}</p>

      <ul className="space-y-3">
        {datos.categorias.map((item) => (
          <li key={item.categoria_id}>
            <div className="flex items-baseline justify-between gap-3 text-sm">
              <span className="font-medium text-slate-800">
                {item.nombre}
                {item.tipo_costo === 'fijo' && <span className="ml-1.5 text-xs font-normal text-slate-500">(fijo)</span>}
              </span>
              <span className="text-slate-600">
                {formatoMoneda(item.total)} · {formatoPorcentaje(item.porcentaje)}
              </span>
            </div>
            {/* Barra proporcional al porcentaje; el dato real está en el texto de arriba */}
            <div className="mt-1 h-2 overflow-hidden rounded-full bg-slate-100" aria-hidden="true">
              <div
                className={`h-full rounded-full ${item.tipo_costo === 'fijo' ? 'bg-slate-600' : 'bg-brand'}`}
                style={{ width: `${Math.min(100, Math.max(0, item.porcentaje))}%` }}
              />
            </div>
          </li>
        ))}
      </ul>

      <dl className="mt-4 grid grid-cols-2 gap-3 border-t border-slate-100 pt-3 text-sm">
        <div>
          <dt className="text-slate-500">Gastos fijos</dt>
          <dd className="font-medium text-slate-900">{formatoMoneda(datos.total_fijo)}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Gastos variables</dt>
          <dd className="font-medium text-slate-900">{formatoMoneda(datos.total_variable)}</dd>
        </div>
      </dl>
    </TarjetaIndicador>
  )
}
