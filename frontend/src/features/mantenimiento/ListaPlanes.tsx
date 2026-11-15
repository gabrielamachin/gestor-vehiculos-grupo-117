import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { useAvisos } from '../../shared/mensajes/useAvisos'
import { useConfirmar } from '../../shared/mensajes/useConfirmar'
import { formatoKm } from '../../shared/formato'
import { eliminarPlan, listarPlanes } from './api'
import type { PlanMantenimiento } from './tipos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; planes: PlanMantenimiento[] }

interface Props {
  vehiculoId: string
  /** Se invoca después de eliminar un plan, para que el resto de la pantalla (indicadores) se actualice. */
  alCambiar: () => void
}

export function ListaPlanes({ vehiculoId, alCambiar }: Props) {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })
  const [eliminando, setEliminando] = useState<string | null>(null)
  const avisos = useAvisos()
  const confirmar = useConfirmar()

  useEffect(() => {
    let cancelado = false
    listarPlanes(vehiculoId)
      .then((planes) => {
        if (!cancelado) setEstado({ tipo: 'ok', planes })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [vehiculoId])

  async function eliminar(plan: PlanMantenimiento) {
    const confirmado = await confirmar({
      titulo: `¿Eliminar el plan "${plan.nombre}"?`,
      mensaje: 'Los gastos asociados se conservan, pero dejan de estar vinculados a este plan.',
      textoConfirmar: 'Eliminar',
      peligro: true,
    })
    if (!confirmado) return

    setEliminando(plan.id)
    try {
      await eliminarPlan(plan.id)
      setEstado((anterior) =>
        anterior.tipo === 'ok' ? { ...anterior, planes: anterior.planes.filter((p) => p.id !== plan.id) } : anterior,
      )
      alCambiar()
      avisos.exito('Plan eliminado')
    } catch (e) {
      avisos.error(mensajeDeError(e))
    } finally {
      setEliminando(null)
    }
  }

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando planes…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  if (estado.planes.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-center text-sm text-slate-500">
        Todavía no definiste planes de mantenimiento. Agregá uno (por ejemplo, cambio de aceite cada 10.000 km) para saber cuándo
        toca el próximo.
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <ul className="divide-y divide-slate-100 rounded-xl border border-slate-200 bg-white shadow-sm">
        {estado.planes.map((plan) => (
          <li key={plan.id} className="p-4">
            <p className="font-medium text-slate-900">{plan.nombre}</p>
            <p className="text-sm text-slate-500">Se repite cada {formatoKm(plan.intervalo_km)}</p>
            <div className="mt-2 flex gap-4 text-sm">
              <Link to={`/planes/${plan.id}/editar`} className="font-medium text-brand hover:underline">
                Editar
              </Link>
              <button
                type="button"
                onClick={() => void eliminar(plan)}
                disabled={eliminando === plan.id}
                className="font-medium text-red-600 hover:underline disabled:opacity-50"
              >
                {eliminando === plan.id ? 'Eliminando…' : 'Eliminar'}
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
