import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { BotonEnlace } from '../../shared/componentes/BotonEnlace'
import { formatoKm } from '../../shared/formato'
import { useAvisos } from '../../shared/mensajes/useAvisos'
import { useConfirmar } from '../../shared/mensajes/useConfirmar'
import { listarGastos } from '../gastos/api'
import { ListaGastos } from '../gastos/ListaGastos'
import { Dashboard } from '../indicadores/Dashboard'
import { listarLecturas } from '../kilometraje/api'
import { ListaLecturas } from '../kilometraje/ListaLecturas'
import { listarPlanes } from '../mantenimiento/api'
import { ListaPlanes } from '../mantenimiento/ListaPlanes'
import { eliminarVehiculo as eliminarVehiculoEnApi, obtenerVehiculo } from './api'
import type { Vehiculo } from './tipos'
import { IconoEliminar, IconoLapiz } from '../../shared/componentes/Iconos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; vehiculo: Vehiculo }

const cantidad = (n: number, singular: string, plural: string) => `${n} ${n === 1 ? singular : plural}`

function DetalleVehiculo({ id }: { id: string }) {
  const navigate = useNavigate()
  const confirmar = useConfirmar()
  const avisos = useAvisos()
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })
  const [eliminando, setEliminando] = useState(false)
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

  // Borrar un vehículo borra también todo lo suyo (ON DELETE CASCADE): se cuenta lo que se perdería y, si hay datos,
  // se pide escribir el alias para confirmar.
  async function eliminar(vehiculo: Vehiculo) {
    setEliminando(true)
    try {
      let detalle = 'Se eliminarán también todos sus gastos, lecturas de kilometraje y planes de mantenimiento.'
      let hayDatos = true
      try {
        const [gastos, lecturas, planes] = await Promise.all([listarGastos(id), listarLecturas(id), listarPlanes(id)])
        hayDatos = gastos.length + lecturas.length + planes.length > 0
        detalle = hayDatos
          ? `Se eliminarán también ${cantidad(gastos.length, 'gasto', 'gastos')}, ${cantidad(lecturas.length, 'lectura de kilometraje', 'lecturas de kilometraje')} y ${cantidad(planes.length, 'plan de mantenimiento', 'planes de mantenimiento')}.`
          : 'Este vehículo todavía no tiene gastos, lecturas ni planes.'
      } catch {
        /* sin el detalle exacto se usa el texto genérico y se pide escribir el alias igual */
      }

      const confirmado = await confirmar({
        titulo: `¿Eliminar "${vehiculo.alias}"?`,
        mensaje: `${detalle} Esta acción no se puede deshacer.`,
        textoConfirmar: 'Eliminar vehículo',
        peligro: true,
        escribir: hayDatos ? vehiculo.alias : undefined,
      })
      if (!confirmado) return

      await eliminarVehiculoEnApi(vehiculo.id)
      avisos.exito('Vehículo eliminado')
      navigate('/')
    } catch (e) {
      avisos.error(mensajeDeError(e))
    } finally {
      setEliminando(false)
    }
  }

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
          <div className="mt-3 flex items-start justify-between gap-3">
            <div className="min-w-0">
              <h1 className="wrap-break-word text-2xl font-semibold">{estado.vehiculo.alias}</h1>
              <p className="text-sm text-slate-500">Kilometraje inicial: {formatoKm(estado.vehiculo.kilometraje_inicial)}</p>
            </div>
            <Link to={`/vehiculos/${id}/editar`} className="inline-flex shrink-0 items-center gap-1.5 text-sm font-medium text-brand hover:underline">
              <IconoLapiz />
              Editar
            </Link>
          </div>
          <div className="mb-5 mt-4 flex flex-wrap gap-3">
            <BotonEnlace to={`/vehiculos/${id}/gastos/nuevo`}>+ Cargar gasto</BotonEnlace>
            <BotonEnlace to={`/vehiculos/${id}/kilometraje/nuevo`} variante="secundario">
              + Cargar kilometraje
            </BotonEnlace>
          </div>
          {/* key: al cambiar de vehículo, o de versión, se reinicia la carga de indicadores */}
          <Dashboard key={`${id}-${version}`} vehiculoId={id} />

          <h2 className="mb-3 mt-8 text-xl font-semibold">Gastos</h2>
          <ListaGastos vehiculoId={id} alCambiar={alCambiar} />

          <h2 className="mb-3 mt-8 text-xl font-semibold">Kilometraje</h2>
          <ListaLecturas vehiculoId={id} alCambiar={alCambiar} />

          <div className="mb-3 mt-8 flex items-center justify-between gap-3">
            <h2 className="text-xl font-semibold">Planes de mantenimiento</h2>
            <Link to={`/vehiculos/${id}/planes/nuevo`} className="text-sm font-medium text-brand hover:underline">
              + Agregar plan
            </Link>
          </div>
          <ListaPlanes vehiculoId={id} alCambiar={alCambiar} />

          <section className="mt-10 rounded-2xl border border-red-200 bg-red-50 p-4">
            <h2 className="text-sm font-semibold text-red-800">Zona de peligro</h2>
            <p className="mt-1 text-sm text-red-700">
              Eliminar el vehículo borra también todos sus gastos, lecturas de kilometraje y planes de mantenimiento.
            </p>
            <button
              type="button"
              onClick={() => void eliminar(estado.vehiculo)}
              disabled={eliminando}
              className="mt-3 inline-flex min-h-11 items-center justify-center rounded-lg border border-red-300 bg-white px-4 text-sm font-medium text-red-700 transition hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <IconoEliminar className="mr-2 h-4 w-4" />
              {eliminando ? 'Preparando…' : 'Eliminar vehículo'}
            </button>
          </section>
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
