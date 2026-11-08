import { useEffect, useState } from 'react'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { obtenerResumen } from './api'
import { AlertaCombustibleTarjeta } from './AlertaCombustibleTarjeta'
import { CostoPorKmTarjeta } from './CostoPorKmTarjeta'
import { GastoPorCategoriaTarjeta } from './GastoPorCategoriaTarjeta'
import { MantenimientosTarjeta } from './MantenimientosTarjeta'
import { OrientacionTarjeta } from './OrientacionTarjeta'
import type { Resumen } from './tipos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; resumen: Resumen }

/** Indicadores de un vehículo. Usar con `key={vehiculoId}` para que cambiar de vehículo reinicie la carga. */
export function Dashboard({ vehiculoId }: { vehiculoId: string }) {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })

  useEffect(() => {
    let cancelado = false
    obtenerResumen(vehiculoId)
      .then((resumen) => {
        if (!cancelado) setEstado({ tipo: 'ok', resumen })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [vehiculoId])

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Calculando indicadores…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  const { resumen } = estado
  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2">
        <CostoPorKmTarjeta datos={resumen.costo_por_km} />
        <AlertaCombustibleTarjeta datos={resumen.alerta_combustible} />
      </div>
      <GastoPorCategoriaTarjeta datos={resumen.gasto_por_categoria} />
      <MantenimientosTarjeta planes={resumen.proximos_mantenimientos} />
      <OrientacionTarjeta datos={resumen.reparar_o_reemplazar} />
    </div>
  )
}
