import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { PaginaFormulario } from '../../shared/componentes/PaginaFormulario'
import { ConVehiculo } from '../vehiculos/ConVehiculo'
import { obtenerLectura } from './api'
import { FormularioLectura } from './FormularioLectura'
import type { Lectura } from './tipos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; lectura: Lectura }

function ContenidoEditarLectura({ lecturaId }: { lecturaId: string }) {
  const navigate = useNavigate()
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })

  useEffect(() => {
    let cancelado = false
    obtenerLectura(lecturaId)
      .then((lectura) => {
        if (!cancelado) setEstado({ tipo: 'ok', lectura })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [lecturaId])

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando lectura…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  const { lectura } = estado
  const volver = `/vehiculos/${lectura.vehiculo_id}`
  return (
    <ConVehiculo key={lectura.vehiculo_id} id={lectura.vehiculo_id}>
      {(vehiculo) => (
        <PaginaFormulario volverA={volver} textoVolver={vehiculo.alias} titulo="Editar lectura" subtitulo={vehiculo.alias}>
          <FormularioLectura vehiculo={vehiculo} lectura={lectura} alGuardar={() => navigate(volver)} />
        </PaginaFormulario>
      )}
    </ConVehiculo>
  )
}

export function PaginaEditarLectura() {
  const { lecturaId } = useParams<{ lecturaId: string }>()
  if (lecturaId === undefined) return <NoEncontrada />
  return <ContenidoEditarLectura key={lecturaId} lecturaId={lecturaId} />
}
