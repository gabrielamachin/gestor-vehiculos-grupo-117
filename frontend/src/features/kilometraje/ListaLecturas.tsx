import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { Insignia } from '../../shared/componentes/Insignia'
import { formatoFecha, formatoKm } from '../../shared/formato'
import { eliminarLectura, listarLecturas } from './api'
import type { Lectura } from './tipos'

const CANTIDAD_INICIAL = 5

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; lecturas: Lectura[] }

interface Props {
  vehiculoId: string
  /** Se invoca después de eliminar una lectura, para que el resto de la pantalla (indicadores) se actualice. */
  alCambiar: () => void
}

export function ListaLecturas({ vehiculoId, alCambiar }: Props) {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })
  const [mostrarTodas, setMostrarTodas] = useState(false)
  const [eliminando, setEliminando] = useState<string | null>(null)
  const [errorAccion, setErrorAccion] = useState<string | null>(null)

  useEffect(() => {
    let cancelado = false
    listarLecturas(vehiculoId)
      .then((lecturas) => {
        if (!cancelado) setEstado({ tipo: 'ok', lecturas })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [vehiculoId])

  async function eliminar(lectura: Lectura) {
    if (!window.confirm('¿Eliminar esta lectura de kilometraje? Esta acción no se puede deshacer.')) return
    setErrorAccion(null)
    setEliminando(lectura.id)
    try {
      await eliminarLectura(lectura.id)
      setEstado((anterior) =>
        anterior.tipo === 'ok' ? { ...anterior, lecturas: anterior.lecturas.filter((l) => l.id !== lectura.id) } : anterior,
      )
      alCambiar()
    } catch (e) {
      setErrorAccion(mensajeDeError(e))
    } finally {
      setEliminando(null)
    }
  }

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando lecturas…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  if (estado.lecturas.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-center text-sm text-slate-500">
        Todavía no cargaste lecturas de kilometraje. Sin ellas no se puede calcular el costo por kilómetro.
      </div>
    )
  }

  const visibles = mostrarTodas ? estado.lecturas : estado.lecturas.slice(0, CANTIDAD_INICIAL)

  return (
    <div className="space-y-3">
      {errorAccion && <Alerta>{errorAccion}</Alerta>}

      <ul className="divide-y divide-slate-100 rounded-xl border border-slate-200 bg-white shadow-sm">
        {visibles.map((lectura, posicion) => (
          <li key={lectura.id} className="p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="font-semibold text-slate-900">{formatoKm(lectura.kilometraje)}</p>
                <p className="text-sm text-slate-500">{formatoFecha(lectura.fecha)}</p>
              </div>
              {/* La lista viene de la más reciente a la más antigua: la primera es el kilometraje actual */}
              {posicion === 0 && <Insignia tono="ok">Actual</Insignia>}
            </div>
            <div className="mt-2 flex gap-4 text-sm">
              <Link to={`/kilometraje/${lectura.id}/editar`} className="font-medium text-brand hover:underline">
                Editar
              </Link>
              <button
                type="button"
                onClick={() => void eliminar(lectura)}
                disabled={eliminando === lectura.id}
                className="font-medium text-red-600 hover:underline disabled:opacity-50"
              >
                {eliminando === lectura.id ? 'Eliminando…' : 'Eliminar'}
              </button>
            </div>
          </li>
        ))}
      </ul>

      {!mostrarTodas && estado.lecturas.length > CANTIDAD_INICIAL && (
        <button type="button" onClick={() => setMostrarTodas(true)} className="text-sm font-medium text-brand hover:underline">
          Ver todas ({estado.lecturas.length})
        </button>
      )}
    </div>
  )
}
