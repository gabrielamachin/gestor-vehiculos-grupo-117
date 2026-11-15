import { useState } from 'react'
import type { FormEvent } from 'react'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { Boton } from '../../shared/componentes/Boton'
import { BotonEnlace } from '../../shared/componentes/BotonEnlace'
import { Campo } from '../../shared/componentes/Campo'
import { useAvisos } from '../../shared/mensajes/useAvisos'
import type { Vehiculo } from '../vehiculos/tipos'
import { actualizarPlan, crearPlan } from './api'
import type { PlanMantenimiento } from './tipos'

// Mismo formato que NUMERIC(10,2) de la base: hasta 8 enteros y 2 decimales, sin signo.
const FORMATO_KM = /^(\d{1,8}(\.\d{1,2})?|\.\d{1,2})$/

interface Props {
  vehiculo: Vehiculo
  /** Si se informa, el formulario edita ese plan; si no, crea uno nuevo. */
  plan?: PlanMantenimiento
  alGuardar: () => void
}

export function FormularioPlan({ vehiculo, plan, alGuardar }: Props) {
  const avisos = useAvisos()
  const [nombre, setNombre] = useState(plan?.nombre ?? '')
  const [intervalo, setIntervalo] = useState(plan === undefined ? '' : String(plan.intervalo_km))
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  // Primera capa de validación (la API y la base validan de nuevo: ver docs/esquema-db.md, sección 6).
  function validar(): string | null {
    if (nombre.trim() === '') return 'Ingresá el nombre del mantenimiento.'
    if (!FORMATO_KM.test(intervalo) || Number(intervalo) <= 0) {
      return 'Ingresá cada cuántos kilómetros se repite: un número mayor a cero, con hasta 2 decimales.'
    }
    return null
  }

  async function alEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    const problema = validar()
    if (problema !== null) {
      setError(problema)
      return
    }
    const cambios = { nombre: nombre.trim(), intervalo_km: Number(intervalo) }

    setError(null)
    setEnviando(true)
    try {
      if (plan) await actualizarPlan(plan.id, cambios)
      else await crearPlan({ vehiculo_id: vehiculo.id, ...cambios })
      avisos.exito(plan ? 'Plan actualizado' : 'Plan guardado')
      alGuardar()
    } catch (e) {
      setError(mensajeDeError(e))
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={alEnviar} noValidate className="space-y-4">
      <Campo
        etiqueta="Qué se mantiene"
        nombre="nombre"
        placeholder="Ej.: Cambio de aceite"
        maxLength={100}
        required
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />
      <Campo
        etiqueta="Se repite cada (km)"
        nombre="intervalo"
        type="number"
        inputMode="decimal"
        min="0"
        step="any"
        required
        placeholder="Ej.: 10000"
        ayuda="Con este dato se estima cuándo toca el próximo mantenimiento."
        value={intervalo}
        onChange={(e) => setIntervalo(e.target.value)}
      />

      {error && <Alerta>{error}</Alerta>}

      <div className="flex flex-col gap-3 sm:flex-row-reverse">
        <Boton type="submit" cargando={enviando} className="sm:flex-1">
          {plan ? 'Guardar cambios' : 'Guardar plan'}
        </Boton>
        <BotonEnlace to={`/vehiculos/${vehiculo.id}`} variante="secundario" className="sm:flex-1">
          Cancelar
        </BotonEnlace>
      </div>
    </form>
  )
}
