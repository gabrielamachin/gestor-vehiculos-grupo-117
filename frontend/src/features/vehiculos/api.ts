import { solicitar } from '../../shared/api/cliente'
import type { Vehiculo } from './tipos'

export function listarVehiculos(): Promise<Vehiculo[]> {
  return solicitar<Vehiculo[]>('/vehiculos')
}

export function obtenerVehiculo(id: string): Promise<Vehiculo> {
  return solicitar<Vehiculo>(`/vehiculos/${id}`)
}
