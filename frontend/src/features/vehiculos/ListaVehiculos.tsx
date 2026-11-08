import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { formatoKm } from '../../shared/formato'
import { listarVehiculos } from './api'
import type { Vehiculo } from './tipos'

type Estado =
  | { tipo: 'cargando' }
  | { tipo: 'error'; mensaje: string }
  | { tipo: 'ok'; vehiculos: Vehiculo[] }

export function ListaVehiculos() {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })

  useEffect(() => {
    let cancelado = false
    listarVehiculos()
      .then((vehiculos) => {
        if (!cancelado) setEstado({ tipo: 'ok', vehiculos })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [])

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando vehículos…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  if (estado.vehiculos.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-center text-sm text-slate-500">
        Todavía no cargaste ningún vehículo.
      </div>
    )
  }

  return (
    <ul className="space-y-3">
      {estado.vehiculos.map((v) => (
        <li key={v.id}>
          <Link
            to={`/vehiculos/${v.id}`}
            className="flex items-center justify-between gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm transition hover:border-brand/40 hover:shadow"
          >
            <span>
              <span className="block font-medium text-slate-900">{v.alias}</span>
              <span className="block text-sm text-slate-500">Kilometraje inicial: {formatoKm(v.kilometraje_inicial)}</span>
            </span>
            <span aria-hidden="true" className="text-slate-400">
              ›
            </span>
          </Link>
        </li>
      ))}
    </ul>
  )
}
