import { useState } from 'react'
import type { FormEvent } from 'react'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { Boton } from '../../shared/componentes/Boton'
import { BotonEnlace } from '../../shared/componentes/BotonEnlace'
import { Campo } from '../../shared/componentes/Campo'
import { formatoKm } from '../../shared/formato'
import { useAvisos } from '../../shared/mensajes/useAvisos'
import { actualizarVehiculo } from './api'
import type { Vehiculo } from './tipos'

export function FormularioAlias({ vehiculo, alGuardar }: { vehiculo: Vehiculo; alGuardar: () => void }) {
  const avisos = useAvisos()
  const [alias, setAlias] = useState(vehiculo.alias)
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  async function alEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    const nuevo = alias.trim()
    if (nuevo === '') {
      setError('Ingresá un alias para identificar el vehículo.')
      return
    }
    if (nuevo === vehiculo.alias) {
      alGuardar() // no hay nada que cambiar
      return
    }

    setError(null)
    setEnviando(true)
    try {
      await actualizarVehiculo(vehiculo.id, { alias: nuevo })
      avisos.exito('Vehículo actualizado')
      alGuardar()
    } catch (e) {
      setError(mensajeDeError(e)) // p. ej. "Ya tenés un vehículo con ese alias"
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={alEnviar} noValidate className="space-y-4">
      <Campo etiqueta="Alias" nombre="alias" maxLength={100} required value={alias} onChange={(e) => setAlias(e.target.value)} />
      <p className="text-sm text-slate-500">
        Kilometraje inicial: {formatoKm(vehiculo.kilometraje_inicial)}. No se puede modificar: es el punto de partida del costo por
        kilómetro.
      </p>

      {error && <Alerta>{error}</Alerta>}

      <div className="flex flex-col gap-3 sm:flex-row-reverse">
        <Boton type="submit" cargando={enviando} className="sm:flex-1">
          Guardar cambios
        </Boton>
        <BotonEnlace to={`/vehiculos/${vehiculo.id}`} variante="secundario" className="sm:flex-1">
          Cancelar
        </BotonEnlace>
      </div>
    </form>
  )
}
