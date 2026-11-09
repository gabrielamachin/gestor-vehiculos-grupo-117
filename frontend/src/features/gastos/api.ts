import { solicitar } from '../../shared/api/cliente'
import type { Gasto, GastoCambios, GastoNuevo } from './tipos'

/** Gastos del vehículo, del más reciente al más antiguo. */
export function listarGastos(vehiculoId: string): Promise<Gasto[]> {
  return solicitar<Gasto[]>('/gastos', { params: { vehiculo_id: vehiculoId } })
}

export function obtenerGasto(id: string): Promise<Gasto> {
  return solicitar<Gasto>(`/gastos/${id}`)
}

export function crearGasto(datos: GastoNuevo): Promise<Gasto> {
  return solicitar<Gasto>('/gastos', { metodo: 'POST', cuerpo: datos })
}

export function actualizarGasto(id: string, datos: GastoCambios): Promise<Gasto> {
  return solicitar<Gasto>(`/gastos/${id}`, { metodo: 'PUT', cuerpo: datos })
}

export function eliminarGasto(id: string): Promise<void> {
  return solicitar<void>(`/gastos/${id}`, { metodo: 'DELETE' })
}
