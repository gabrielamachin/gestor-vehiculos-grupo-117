import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { Boton } from '../../shared/componentes/Boton'
import { BotonEnlace } from '../../shared/componentes/BotonEnlace'
import { Campo } from '../../shared/componentes/Campo'
import { useAvisos } from '../../shared/mensajes/useAvisos'
import { fechaDeHoy, formatoFecha, formatoKm } from '../../shared/formato'
import type { Vehiculo } from '../vehiculos/tipos'
import { actualizarLectura, crearLectura, listarLecturas } from './api'
import type { Lectura } from './tipos'

// Mismo formato que NUMERIC(10,2) de la base: hasta 8 enteros y 2 decimales, sin signo.
const FORMATO_KM = /^(\d{1,8}(\.\d{1,2})?|\.\d{1,2})$/

interface Props {
  vehiculo: Vehiculo
  /** Si se informa, el formulario edita esa lectura; si no, crea una nueva. */
  lectura?: Lectura
  alGuardar: () => void
}

export function FormularioLectura({ vehiculo, lectura, alGuardar }: Props) {
  const avisos = useAvisos()
  const editando = lectura !== undefined
  const [kilometraje, setKilometraje] = useState(lectura === undefined ? '' : String(lectura.kilometraje))
  const [fecha, setFecha] = useState(lectura?.fecha ?? fechaDeHoy())
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)
  // Referencia para quien carga: la última lectura (undefined mientras se consulta o si falla la consulta).
  const [ultima, setUltima] = useState<Lectura | null | undefined>(undefined)

  useEffect(() => {
    if (editando) return
    let cancelado = false
    listarLecturas(vehiculo.id)
      .then((lecturas) => {
        if (!cancelado) setUltima(lecturas[0] ?? null)
      })
      .catch(() => {
        /* la referencia es solo una ayuda: si falla no se muestra */
      })
    return () => {
      cancelado = true
    }
  }, [vehiculo.id, editando])

  let ayuda: string | undefined
  if (ultima !== undefined) {
    ayuda =
      ultima === null
        ? `Todavía no hay lecturas. El kilometraje inicial del vehículo es ${formatoKm(vehiculo.kilometraje_inicial)}.`
        : `Última lectura: ${formatoKm(ultima.kilometraje)} (${formatoFecha(ultima.fecha)}).`
  }

  // Primera capa de validación. La coherencia con las demás lecturas (el odómetro no retrocede) la valida el
  // servicio del backend: es una regla entre filas que ni siquiera la base puede expresar (docs/esquema-db.md, sección 6).
  function validar(): string | null {
    if (!FORMATO_KM.test(kilometraje)) return 'Ingresá el kilometraje (un número sin signo, con hasta 2 decimales).'
    if (Number(kilometraje) < vehiculo.kilometraje_inicial) {
      return `El kilometraje no puede ser menor al inicial del vehículo (${formatoKm(vehiculo.kilometraje_inicial)}).`
    }
    if (fecha === '') return 'Ingresá la fecha de la lectura.'
    if (fecha > fechaDeHoy()) return 'La fecha no puede ser futura.'
    return null
  }

  async function alEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    const problema = validar()
    if (problema !== null) {
      setError(problema)
      return
    }
    const cambios = { fecha, kilometraje: Number(kilometraje) }

    setError(null)
    setEnviando(true)
    try {
      if (lectura) await actualizarLectura(lectura.id, cambios)
      else await crearLectura({ vehiculo_id: vehiculo.id, ...cambios })
      avisos.exito(lectura ? 'Lectura actualizada' : 'Lectura guardada')
      alGuardar()
    } catch (e) {
      setError(mensajeDeError(e))
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={alEnviar} noValidate className="space-y-4">
      <Campo
        etiqueta="Kilometraje actual del odómetro"
        nombre="kilometraje"
        type="number"
        inputMode="decimal"
        min="0"
        step="any"
        required
        ayuda={ayuda}
        value={kilometraje}
        onChange={(e) => setKilometraje(e.target.value)}
      />
      <Campo
        etiqueta="Fecha de la lectura"
        nombre="fecha"
        type="date"
        max={fechaDeHoy()}
        required
        value={fecha}
        onChange={(e) => setFecha(e.target.value)}
      />

      {error && <Alerta>{error}</Alerta>}

      <div className="flex flex-col gap-3 sm:flex-row-reverse">
        <Boton type="submit" cargando={enviando} className="sm:flex-1">
          {editando ? 'Guardar cambios' : 'Guardar lectura'}
        </Boton>
        <BotonEnlace to={`/vehiculos/${vehiculo.id}`} variante="secundario" className="sm:flex-1">
          Cancelar
        </BotonEnlace>
      </div>
    </form>
  )
}
