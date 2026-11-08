import { formatoKm } from '../../shared/formato'
import { Insignia } from '../../shared/componentes/Insignia'
import type { Tono } from '../../shared/componentes/TarjetaIndicador'
import { TarjetaIndicador } from '../../shared/componentes/TarjetaIndicador'
import type { ProximoMantenimiento } from './tipos'

const INSIGNIA: Record<ProximoMantenimiento['estado'], { tono: Tono; texto: string }> = {
  vencido: { tono: 'peligro', texto: 'Vencido' },
  proximo: { tono: 'alerta', texto: 'Próximo' },
  al_dia: { tono: 'ok', texto: 'Al día' },
  sin_lecturas: { tono: 'neutro', texto: 'Sin datos' },
}

function detalle(plan: ProximoMantenimiento): string {
  const objetivo = formatoKm(plan.proximo_km)
  if (plan.km_restantes === null) return `Le toca a los ${objetivo}. Cargá una lectura de kilometraje para ver cuánto falta.`
  if (plan.km_restantes < 0) return `Pasaste el kilometraje previsto (${objetivo}) por ${formatoKm(-plan.km_restantes)}.`
  if (plan.km_restantes === 0) return `Toca hacerlo ahora (${objetivo}).`
  return `Faltan ${formatoKm(plan.km_restantes)} (a los ${objetivo}).`
}

export function MantenimientosTarjeta({ planes }: { planes: ProximoMantenimiento[] }) {
  if (planes.length === 0) {
    return (
      <TarjetaIndicador titulo="Próximos mantenimientos">
        <p className="text-sm text-slate-500">Todavía no definiste planes de mantenimiento para este vehículo.</p>
      </TarjetaIndicador>
    )
  }

  return (
    <TarjetaIndicador titulo="Próximos mantenimientos">
      <ul className="divide-y divide-slate-100">
        {planes.map((plan) => {
          const insignia = INSIGNIA[plan.estado]
          return (
            <li key={plan.plan_id} className="py-3 first:pt-0 last:pb-0">
              <div className="flex items-center justify-between gap-3">
                <span className="font-medium text-slate-900">{plan.nombre}</span>
                <Insignia tono={insignia.tono}>{insignia.texto}</Insignia>
              </div>
              <p className="mt-1 text-sm text-slate-600">{detalle(plan)}</p>
              {plan.base === 'multiplos' && (
                <p className="mt-0.5 text-xs text-slate-400">
                  Estimado a partir de cada {formatoKm(plan.intervalo_km)}: todavía no registraste este mantenimiento.
                </p>
              )}
            </li>
          )
        })}
      </ul>
    </TarjetaIndicador>
  )
}
