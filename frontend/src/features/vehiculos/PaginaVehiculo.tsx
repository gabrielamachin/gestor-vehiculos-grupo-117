import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { BotonEnlace } from '../../shared/componentes/BotonEnlace'
import { formatoKm } from '../../shared/formato'
import { ListaGastos } from '../gastos/ListaGastos'
import { Dashboard } from '../indicadores/Dashboard'
import { ListaLecturas } from '../kilometraje/ListaLecturas'
import { ListaPlanes } from '../mantenimiento/ListaPlanes'
import { obtenerVehiculo } from './api'
import type { Vehiculo } from './tipos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; vehiculo: Vehiculo }

function DetalleVehiculo({ id }: { id: string }) {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })
  // Se incrementa al eliminar un gasto, una lectura o un plan: cambia la key del dashboard y fuerza a recalcular los indicadores.
  const [version, setVersion] = useState(0)
  const alCambiar = () => setVersion((v) => v + 1)

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
          <p className="text-sm text-slate-500">Kilometraje inicial: {formatoKm(estado.vehiculo.kilometraje_inicial)}</p>
          <div className="mb-5 mt-4 flex flex-wrap gap-3">
            <BotonEnlace to={`/vehiculos/${id}/gastos/nuevo`}>+ Cargar gasto</BotonEnlace>
            <BotonEnlace to={`/vehiculos/${id}/kilometraje/nuevo`} variante="secundario">
              + Cargar kilometraje
            </BotonEnlace>
          </div>
          {/* key: al cambiar de vehículo, o de versión, se reinicia la carga de indicadores */}
          <Dashboard key={`${id}-${version}`} vehiculoId={id} />

          <h2 className="mb-3 mt-8 text-lg font-semibold">Gastos</h2>
          <ListaGastos vehiculoId={id} alCambiar={alCambiar} />

          <h2 className="mb-3 mt-8 text-lg font-semibold">Kilometraje</h2>
          <ListaLecturas vehiculoId={id} alCambiar={alCambiar} />

          <div className="mb-3 mt-8 flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold">Planes de mantenimiento</h2>
            <Link to={`/vehiculos/${id}/planes/nuevo`} className="text-sm font-medium text-brand hover:underline">
              + Agregar plan
            </Link>
          </div>
          <ListaPlanes vehiculoId={id} alCambiar={alCambiar} />
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
