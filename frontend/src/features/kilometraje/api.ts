import { solicitar } from '../../shared/api/cliente'
import type { Lectura, LecturaCambios, LecturaNueva } from './tipos'

/** Lecturas del vehículo, de la más reciente a la más antigua. */
export function listarLecturas(vehiculoId: string): Promise<Lectura[]> {
  return solicitar<Lectura[]>('/kilometraje', { params: { vehiculo_id: vehiculoId } })
}

export function obtenerLectura(id: string): Promise<Lectura> {
  return solicitar<Lectura>(`/kilometraje/${id}`)
}

export function crearLectura(datos: LecturaNueva): Promise<Lectura> {
  return solicitar<Lectura>('/kilometraje', { metodo: 'POST', cuerpo: datos })
}

export function actualizarLectura(id: string, datos: LecturaCambios): Promise<Lectura> {
  return solicitar<Lectura>(`/kilometraje/${id}`, { metodo: 'PUT', cuerpo: datos })
}

export function eliminarLectura(id: string): Promise<void> {
  return solicitar<void>(`/kilometraje/${id}`, { metodo: 'DELETE' })
}
