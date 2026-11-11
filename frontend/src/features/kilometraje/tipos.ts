export interface Lectura {
  id: string
  vehiculo_id: string
  fecha: string
  kilometraje: number
}

/** Datos editables de una lectura (la lectura no cambia de vehículo). */
export interface LecturaCambios {
  fecha: string
  kilometraje: number
}

export interface LecturaNueva extends LecturaCambios {
  vehiculo_id: string
}
