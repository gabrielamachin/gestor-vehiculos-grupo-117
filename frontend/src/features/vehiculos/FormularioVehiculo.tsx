import { useState } from 'react'
import type { FormEvent } from 'react'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { Boton } from '../../shared/componentes/Boton'
import { BotonEnlace } from '../../shared/componentes/BotonEnlace'
import { Campo } from '../../shared/componentes/Campo'
import { useAvisos } from '../../shared/mensajes/useAvisos'
import { crearVehiculo } from './api'
import type { Vehiculo } from './tipos'

// Mismo formato que NUMERIC(10,2) de la base: hasta 8 enteros y 2 decimales, sin signo.
const FORMATO_KM = /^(\d{1,8}(\.\d{1,2})?|\.\d{1,2})$/

export function FormularioVehiculo({ alCrear }: { alCrear: (vehiculo: Vehiculo) => void }) {
  const avisos = useAvisos()
  const [alias, setAlias] = useState('')
  const [kilometraje, setKilometraje] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  // Primera capa de validación (la API y la base validan de nuevo: ver docs/esquema-db.md, sección 6).
  function validar(): string | null {
    if (alias.trim() === '') return 'Ingresá un alias para identificar el vehículo.'
    if (!FORMATO_KM.test(kilometraje)) return 'Ingresá el kilometraje actual (un número sin signo, con hasta 2 decimales).'
    return null
  }

  async function alEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    const problema = validar()
    if (problema !== null) {
      setError(problema)
      return
    }
    setError(null)
    setEnviando(true)
    try {
      const vehiculo = await crearVehiculo({ alias: alias.trim(), kilometraje_inicial: Number(kilometraje) })
      avisos.exito('Vehículo agregado')
      alCrear(vehiculo)
    } catch (e) {
      setError(mensajeDeError(e))
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={alEnviar} noValidate className="space-y-4">
      <Campo
        etiqueta="Alias"
        nombre="alias"
        placeholder="Ej.: Toyota Corolla"
        maxLength={100}
        required
        value={alias}
        onChange={(e) => setAlias(e.target.value)}
      />
      <Campo
        etiqueta="Kilometraje actual"
        nombre="kilometraje"
        type="number"
        inputMode="decimal"
        min="0"
        step="any"
        required
        ayuda="Es el punto de partida para calcular el costo por kilómetro. No se puede modificar después."
        value={kilometraje}
        onChange={(e) => setKilometraje(e.target.value)}
      />
      {error && <Alerta>{error}</Alerta>}
      <div className="flex flex-col gap-3 sm:flex-row-reverse">
        <Boton type="submit" cargando={enviando} className="sm:flex-1">
          Guardar vehículo
        </Boton>
        <BotonEnlace to="/" variante="secundario" className="sm:flex-1">
          Cancelar
        </BotonEnlace>
      </div>
    </form>
  )
}
