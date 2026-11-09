import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { formatoFecha, formatoMoneda } from '../../shared/formato'
import { listarCategorias } from '../categorias/api'
import type { Categoria } from '../categorias/tipos'
import { eliminarGasto, listarGastos } from './api'
import type { Gasto } from './tipos'

const CANTIDAD_INICIAL = 10

type Estado =
  | { tipo: 'cargando' }
  | { tipo: 'error'; mensaje: string }
  | { tipo: 'ok'; gastos: Gasto[]; categorias: Categoria[] }

interface Props {
  vehiculoId: string
  /** Se invoca después de eliminar un gasto, para que el resto de la pantalla (indicadores) se actualice. */
  alCambiar: () => void
}

export function ListaGastos({ vehiculoId, alCambiar }: Props) {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })
  const [mostrarTodos, setMostrarTodos] = useState(false)
  const [eliminando, setEliminando] = useState<string | null>(null)
  const [errorAccion, setErrorAccion] = useState<string | null>(null)

  useEffect(() => {
    let cancelado = false
    Promise.all([listarGastos(vehiculoId), listarCategorias()])
      .then(([gastos, categorias]) => {
        if (!cancelado) setEstado({ tipo: 'ok', gastos, categorias })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [vehiculoId])

  async function eliminar(gasto: Gasto) {
    if (!window.confirm('¿Eliminar este gasto? Esta acción no se puede deshacer.')) return
    setErrorAccion(null)
    setEliminando(gasto.id)
    try {
      await eliminarGasto(gasto.id)
      setEstado((anterior) =>
        anterior.tipo === 'ok' ? { ...anterior, gastos: anterior.gastos.filter((g) => g.id !== gasto.id) } : anterior,
      )
      alCambiar()
    } catch (e) {
      setErrorAccion(mensajeDeError(e))
    } finally {
      setEliminando(null)
    }
  }

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando gastos…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  if (estado.gastos.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-center text-sm text-slate-500">
        Todavía no cargaste gastos para este vehículo.
      </div>
    )
  }

  const nombres = new Map(estado.categorias.map((c) => [c.id, c.nombre]))
  const visibles = mostrarTodos ? estado.gastos : estado.gastos.slice(0, CANTIDAD_INICIAL)

  return (
    <div className="space-y-3">
      {errorAccion && <Alerta>{errorAccion}</Alerta>}

      <ul className="divide-y divide-slate-100 rounded-xl border border-slate-200 bg-white shadow-sm">
        {visibles.map((gasto) => (
          <li key={gasto.id} className="p-4">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="font-medium text-slate-900">{nombres.get(gasto.categoria_id) ?? 'Sin categoría'}</p>
                <p className="text-sm text-slate-500">{formatoFecha(gasto.fecha)}</p>
                {gasto.descripcion && <p className="mt-1 break-words text-sm text-slate-600">{gasto.descripcion}</p>}
              </div>
              <p className="shrink-0 font-semibold text-slate-900">{formatoMoneda(gasto.monto, 2)}</p>
            </div>
            <div className="mt-2 flex gap-4 text-sm">
              <Link to={`/gastos/${gasto.id}/editar`} className="font-medium text-brand hover:underline">
                Editar
              </Link>
              <button
                type="button"
                onClick={() => void eliminar(gasto)}
                disabled={eliminando === gasto.id}
                className="font-medium text-red-600 hover:underline disabled:opacity-50"
              >
                {eliminando === gasto.id ? 'Eliminando…' : 'Eliminar'}
              </button>
            </div>
          </li>
        ))}
      </ul>

      {!mostrarTodos && estado.gastos.length > CANTIDAD_INICIAL && (
        <button
          type="button"
          onClick={() => setMostrarTodos(true)}
          className="text-sm font-medium text-brand hover:underline"
        >
          Ver todos ({estado.gastos.length})
        </button>
      )}
    </div>
  )
}
