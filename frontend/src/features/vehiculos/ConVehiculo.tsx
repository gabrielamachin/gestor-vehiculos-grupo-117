import { useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { obtenerVehiculo } from './api'
import type { Vehiculo } from './tipos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; vehiculo: Vehiculo }

/** Carga el vehículo `id` y muestra `children(vehiculo)` cuando está listo. Usar con `key={id}`. */
export function ConVehiculo({ id, children }: { id: string; children: (vehiculo: Vehiculo) => ReactNode }) {
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

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando vehículo…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>
  return <>{children(estado.vehiculo)}</>
}
