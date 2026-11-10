import { solicitar } from '../../shared/api/cliente'
import type { PlanCambios, PlanMantenimiento, PlanNuevo } from './tipos'

/** Planes del vehículo, ordenados por nombre. */
export function listarPlanes(vehiculoId: string): Promise<PlanMantenimiento[]> {
  return solicitar<PlanMantenimiento[]>('/mantenimiento', { params: { vehiculo_id: vehiculoId } })
}

export function obtenerPlan(id: string): Promise<PlanMantenimiento> {
  return solicitar<PlanMantenimiento>(`/mantenimiento/${id}`)
}

export function crearPlan(datos: PlanNuevo): Promise<PlanMantenimiento> {
  return solicitar<PlanMantenimiento>('/mantenimiento', { metodo: 'POST', cuerpo: datos })
}

export function actualizarPlan(id: string, datos: PlanCambios): Promise<PlanMantenimiento> {
  return solicitar<PlanMantenimiento>(`/mantenimiento/${id}`, { metodo: 'PUT', cuerpo: datos })
}

export function eliminarPlan(id: string): Promise<void> {
  return solicitar<void>(`/mantenimiento/${id}`, { metodo: 'DELETE' })
}
