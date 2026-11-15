import { solicitar } from '../../shared/api/cliente'
import type { Vehiculo } from './tipos'

export function listarVehiculos(): Promise<Vehiculo[]> {
  return solicitar<Vehiculo[]>('/vehiculos')
}

export function obtenerVehiculo(id: string): Promise<Vehiculo> {
  return solicitar<Vehiculo>(`/vehiculos/${id}`)
}

export function crearVehiculo(datos: { alias: string; kilometraje_inicial: number }): Promise<Vehiculo> {
  return solicitar<Vehiculo>('/vehiculos', { metodo: 'POST', cuerpo: datos })
}

/** Solo se edita el alias: el kilometraje inicial es la base del costo por km y no se modifica. */
export function actualizarVehiculo(id: string, datos: { alias: string }): Promise<Vehiculo> {
  return solicitar<Vehiculo>(`/vehiculos/${id}`, { metodo: 'PUT', cuerpo: datos })
}

/** Borra el vehículo y, en cascada, sus gastos, lecturas de kilometraje y planes de mantenimiento. */
export function eliminarVehiculo(id: string): Promise<void> {
  return solicitar<void>(`/vehiculos/${id}`, { metodo: 'DELETE' })
}
