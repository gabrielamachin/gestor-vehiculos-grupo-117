import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { formatoKm } from '../../shared/formato'
import { Dashboard } from '../indicadores/Dashboard'
import { obtenerVehiculo } from './api'
import type { Vehiculo } from './tipos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; vehiculo: Vehiculo }

function DetalleVehiculo({ id }: { id: string }) {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })

  useEffect(() => {
    let cancelado = false
    obtenerVehiculo(id)
      .then((vehiculo) => {
        if (!cancelado) setEstado({ tipo: 'ok', vehiculo })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [id])

  return (
    <section>
      <Link to="/" className="text-sm font-medium text-brand hover:underline">
        ← Mis vehículos
      </Link>

      {estado.tipo === 'cargando' && <p className="mt-4 text-sm text-slate-500">Cargando vehículo…</p>}
      {estado.tipo === 'error' && (
        <div className="mt-4">
          <Alerta>{estado.mensaje}</Alerta>
        </div>
      )}
      {estado.tipo === 'ok' && (
        <>
          <h1 className="mt-3 text-xl font-semibold">{estado.vehiculo.alias}</h1>
          <p className="mb-5 text-sm text-slate-500">Kilometraje inicial: {formatoKm(estado.vehiculo.kilometraje_inicial)}</p>
          {/* key: al cambiar de vehículo se reinicia la carga de indicadores */}
          <Dashboard key={id} vehiculoId={id} />
        </>
      )}
    </section>
  )
}

export function PaginaVehiculo() {
  const { id } = useParams<{ id: string }>()
  if (id === undefined) return <NoEncontrada />
  return <DetalleVehiculo key={id} id={id} />
}
