import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { PaginaFormulario } from '../../shared/componentes/PaginaFormulario'
import { ConVehiculo } from '../vehiculos/ConVehiculo'
import { obtenerGasto } from './api'
import { FormularioGasto } from './FormularioGasto'
import type { Gasto } from './tipos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; gasto: Gasto }

function ContenidoEditarGasto({ gastoId }: { gastoId: string }) {
  const navigate = useNavigate()
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })

  useEffect(() => {
    let cancelado = false
    obtenerGasto(gastoId)
      .then((gasto) => {
        if (!cancelado) setEstado({ tipo: 'ok', gasto })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [gastoId])

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando gasto…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  const { gasto } = estado
  const volver = `/vehiculos/${gasto.vehiculo_id}`
  return (
    <ConVehiculo key={gasto.vehiculo_id} id={gasto.vehiculo_id}>
      {(vehiculo) => (
        <PaginaFormulario volverA={volver} textoVolver={vehiculo.alias} titulo="Editar gasto" subtitulo={vehiculo.alias}>
          <FormularioGasto vehiculo={vehiculo} gasto={gasto} alGuardar={() => navigate(volver)} />
        </PaginaFormulario>
      )}
    </ConVehiculo>
  )
}

export function PaginaEditarGasto() {
  const { gastoId } = useParams<{ gastoId: string }>()
  if (gastoId === undefined) return <NoEncontrada />
  return <ContenidoEditarGasto key={gastoId} gastoId={gastoId} />
}
