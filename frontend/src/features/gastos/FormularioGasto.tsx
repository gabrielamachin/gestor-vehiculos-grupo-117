import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { Boton } from '../../shared/componentes/Boton'
import { BotonEnlace } from '../../shared/componentes/BotonEnlace'
import { Campo } from '../../shared/componentes/Campo'
import { Selector } from '../../shared/componentes/Selector'
import { fechaDeHoy, formatoKm } from '../../shared/formato'
import { listarCategorias } from '../categorias/api'
import type { Categoria } from '../categorias/tipos'
import { listarPlanes } from '../mantenimiento/api'
import type { PlanMantenimiento } from '../mantenimiento/tipos'
import type { Vehiculo } from '../vehiculos/tipos'
import { actualizarGasto, crearGasto } from './api'
import type { Gasto, GastoCambios } from './tipos'

// Mismos formatos que NUMERIC(12,2) y NUMERIC(10,2) de la base: sin signo y hasta 2 decimales.
const FORMATO_MONTO = /^(\d{1,10}(\.\d{1,2})?|\.\d{1,2})$/
const FORMATO_KM = /^(\d{1,8}(\.\d{1,2})?|\.\d{1,2})$/

// Acoplamiento consciente con el catálogo: solo esta categoría admite asociar un plan (regla del backend).
const CODIGO_MANTENIMIENTO = 'mantenimiento'

interface Datos {
  categorias: Categoria[]
  planes: PlanMantenimiento[]
}

type Estado = { tipo: 'cargando' } | { tipo: 'error'; mensaje: string } | { tipo: 'ok'; datos: Datos }

interface Props {
  vehiculo: Vehiculo
  /** Si se informa, el formulario edita ese gasto; si no, crea uno nuevo. */
  gasto?: Gasto
  alGuardar: () => void
}

/** Carga las categorías y los planes del vehículo y recién entonces muestra los campos. */
export function FormularioGasto({ vehiculo, gasto, alGuardar }: Props) {
  const [estado, setEstado] = useState<Estado>({ tipo: 'cargando' })

  useEffect(() => {
    let cancelado = false
    Promise.all([listarCategorias(), listarPlanes(vehiculo.id)])
      .then(([categorias, planes]) => {
        if (!cancelado) setEstado({ tipo: 'ok', datos: { categorias, planes } })
      })
      .catch((e) => {
        if (!cancelado) setEstado({ tipo: 'error', mensaje: mensajeDeError(e) })
      })
    return () => {
      cancelado = true
    }
  }, [vehiculo.id])

  if (estado.tipo === 'cargando') return <p className="text-sm text-slate-500">Cargando…</p>
  if (estado.tipo === 'error') return <Alerta>{estado.mensaje}</Alerta>

  return (
    <CamposGasto
      vehiculo={vehiculo}
      gasto={gasto}
      categorias={estado.datos.categorias}
      planes={estado.datos.planes}
      alGuardar={alGuardar}
    />
  )
}

interface PropsCampos extends Props {
  categorias: Categoria[]
  planes: PlanMantenimiento[]
}

function texto(valor: number | null | undefined): string {
  return valor === null || valor === undefined ? '' : String(valor)
}

function CamposGasto({ vehiculo, gasto, categorias, planes, alGuardar }: PropsCampos) {
  const [categoriaId, setCategoriaId] = useState(texto(gasto?.categoria_id))
  const [planId, setPlanId] = useState(gasto?.plan_mantenimiento_id ?? '')
  const [monto, setMonto] = useState(texto(gasto?.monto))
  const [fecha, setFecha] = useState(gasto?.fecha ?? fechaDeHoy())
  const [kilometraje, setKilometraje] = useState(texto(gasto?.kilometraje))
  const [descripcion, setDescripcion] = useState(gasto?.descripcion ?? '')
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  // Categorías activas; al editar se conserva la del gasto aunque se haya desactivado después.
  const disponibles = categorias.filter((c) => c.activa || c.id === gasto?.categoria_id)
  const esMantenimiento = disponibles.find((c) => String(c.id) === categoriaId)?.codigo === CODIGO_MANTENIMIENTO
  const volver = `/vehiculos/${vehiculo.id}`

  function alCambiarCategoria(valor: string) {
    setCategoriaId(valor)
    // Un plan solo corresponde a la categoría Mantenimiento
    if (disponibles.find((c) => String(c.id) === valor)?.codigo !== CODIGO_MANTENIMIENTO) setPlanId('')
  }

  // Primera capa de validación (la API y la base validan de nuevo: ver docs/esquema-db.md, sección 6).
  function validar(): string | null {
    if (categoriaId === '') return 'Elegí una categoría.'
    if (!FORMATO_MONTO.test(monto) || Number(monto) <= 0) return 'Ingresá un monto mayor a cero, con hasta 2 decimales.'
    if (fecha === '') return 'Ingresá la fecha del gasto.'
    if (fecha > fechaDeHoy()) return 'La fecha no puede ser futura.'
    if (kilometraje !== '') {
      if (!FORMATO_KM.test(kilometraje)) return 'El kilometraje debe ser un número sin signo, con hasta 2 decimales.'
      if (Number(kilometraje) < vehiculo.kilometraje_inicial) {
        return `El kilometraje no puede ser menor al inicial del vehículo (${formatoKm(vehiculo.kilometraje_inicial)}).`
      }
    }
    if (planId !== '' && kilometraje === '') return 'Ingresá el kilometraje al que hiciste este mantenimiento.'
    return null
  }

  async function alEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    const problema = validar()
    if (problema !== null) {
      setError(problema)
      return
    }

    const cambios: GastoCambios = {
      categoria_id: Number(categoriaId),
      plan_mantenimiento_id: planId === '' ? null : planId,
      monto: Number(monto),
      fecha,
      kilometraje: kilometraje === '' ? null : Number(kilometraje),
      descripcion: descripcion.trim() === '' ? null : descripcion.trim(),
    }

    setError(null)
    setEnviando(true)
    try {
      if (gasto) await actualizarGasto(gasto.id, cambios)
      else await crearGasto({ vehiculo_id: vehiculo.id, ...cambios })
      alGuardar()
    } catch (e) {
      setError(mensajeDeError(e))
      setEnviando(false)
    }
  }

  return (
    <form onSubmit={alEnviar} noValidate className="space-y-4">
      <Selector etiqueta="Categoría" nombre="categoria" required value={categoriaId} onChange={(e) => alCambiarCategoria(e.target.value)}>
        <option value="">Elegí una categoría</option>
        {disponibles.map((c) => (
          <option key={c.id} value={c.id}>
            {c.nombre}
          </option>
        ))}
      </Selector>

      <Campo
        etiqueta="Monto ($)"
        nombre="monto"
        type="number"
        inputMode="decimal"
        min="0"
        step="0.01"
        required
        value={monto}
        onChange={(e) => setMonto(e.target.value)}
      />

      <Campo
        etiqueta="Fecha"
        nombre="fecha"
        type="date"
        max={fechaDeHoy()}
        required
        value={fecha}
        onChange={(e) => setFecha(e.target.value)}
      />

      {esMantenimiento && (
        <Selector
          etiqueta="Plan de mantenimiento (opcional)"
          nombre="plan"
          value={planId}
          onChange={(e) => setPlanId(e.target.value)}
          ayuda={
            planes.length === 0
              ? 'Todavía no definiste planes de mantenimiento para este vehículo.'
              : 'Si este gasto cumple un plan, se usa para estimar cuándo toca el próximo.'
          }
        >
          <option value="">Ninguno</option>
          {planes.map((p) => (
            <option key={p.id} value={p.id}>
              {p.nombre}
            </option>
          ))}
        </Selector>
      )}

      <Campo
        etiqueta={planId === '' ? 'Kilometraje (opcional)' : 'Kilometraje'}
        nombre="kilometraje"
        type="number"
        inputMode="decimal"
        min="0"
        step="any"
        required={planId !== ''}
        ayuda={planId === '' ? undefined : 'Obligatorio para registrar a qué kilometraje hiciste este mantenimiento.'}
        value={kilometraje}
        onChange={(e) => setKilometraje(e.target.value)}
      />

      <Campo
        etiqueta="Detalle (opcional)"
        nombre="descripcion"
        maxLength={500}
        placeholder="Ej.: Carga completa en YPF"
        value={descripcion}
        onChange={(e) => setDescripcion(e.target.value)}
      />

      {error && <Alerta>{error}</Alerta>}

      <div className="flex flex-col gap-3 sm:flex-row-reverse">
        <Boton type="submit" cargando={enviando} className="sm:flex-1">
          {gasto ? 'Guardar cambios' : 'Guardar gasto'}
        </Boton>
        <BotonEnlace to={volver} variante="secundario" className="sm:flex-1">
          Cancelar
        </BotonEnlace>
      </div>
    </form>
  )
}
