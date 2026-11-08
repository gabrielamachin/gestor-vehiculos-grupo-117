import { solicitar } from '../../shared/api/cliente'
import type { Resumen } from './tipos'

/** Todos los indicadores del vehículo en una sola llamada. */
export function obtenerResumen(vehiculoId: string): Promise<Resumen> {
  return solicitar<Resumen>(`/indicadores/vehiculos/${vehiculoId}/resumen`)
}
