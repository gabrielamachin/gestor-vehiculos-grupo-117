/** Error devuelto por la API (o de conexión: estado 0). El mensaje ya está listo para mostrarse al usuario. */
export class ApiError extends Error {
  readonly estado: number

  constructor(estado: number, mensaje: string) {
    super(mensaje)
    this.name = 'ApiError'
    this.estado = estado
  }
}

interface DetalleValidacion {
  loc?: unknown[]
  msg?: string
}

/** Traduce el cuerpo de error de FastAPI: `{detail: "texto"}` (errores de negocio) o `{detail: [...]}` (validación 422). */
export function mensajeDeRespuesta(estado: number, cuerpo: unknown): string {
  const detalle =
    typeof cuerpo === 'object' && cuerpo !== null && 'detail' in cuerpo
      ? (cuerpo as { detail: unknown }).detail
      : undefined

  if (typeof detalle === 'string') return detalle

  if (Array.isArray(detalle) && detalle.length > 0) {
    const lineas = (detalle as DetalleValidacion[]).map((d) => {
      const campo = d.loc?.[d.loc.length - 1]
      const mensaje = (d.msg ?? 'valor inválido').replace(/^Value error, /, '')
      return typeof campo === 'string' ? `${campo}: ${mensaje}` : mensaje
    })
    return `Revisá los datos ingresados (${lineas.join('; ')}).`
  }

  if (estado >= 500) return 'El servidor tuvo un problema. Intentá de nuevo en unos minutos.'
  return 'Ocurrió un error inesperado.'
}

export function mensajeDeError(error: unknown): string {
  return error instanceof Error ? error.message : 'Ocurrió un error inesperado.'
}
