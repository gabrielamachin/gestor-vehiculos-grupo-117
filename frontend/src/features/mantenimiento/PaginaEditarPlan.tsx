import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { PaginaFormulario } from '../../shared/componentes/PaginaFormulario'
import { ConVehiculo } from '../vehiculos/ConVehiculo'
import { obtenerPlan } from './api'
import { FormularioPlan } from './FormularioPlan'
import type { PlanMantenimiento } from './tipos'

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; plan: PlanMantenimiento }

function ContenidoEditarPlan({ planId }: { planId: string }) {
  const navigate = useNavigate()
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })

  useEffect(() => {
    let cancelado = false
    obtenerPlan(planId)
      .then((plan) => {
        if (!cancelado) setEstado({ tipo: 'ok', plan })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [planId])

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando plan…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  const { plan } = estado
  const volver = `/vehiculos/${plan.vehiculo_id}`
  return (
    <ConVehiculo key={plan.vehiculo_id} id={plan.vehiculo_id}>
      {(vehiculo) => (
        <PaginaFormulario volverA={volver} textoVolver={vehiculo.alias} titulo="Editar plan de mantenimiento" subtitulo={vehiculo.alias}>
          <FormularioPlan vehiculo={vehiculo} plan={plan} alGuardar={() => navigate(volver)} />
        </PaginaFormulario>
      )}
    </ConVehiculo>
  )
}

export function PaginaEditarPlan() {
  const { planId } = useParams<{ planId: string }>()
  if (planId === undefined) return <NoEncontrada />
  return <ContenidoEditarPlan key={planId} planId={planId} />
}
