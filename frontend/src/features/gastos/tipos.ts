export interface Gasto {
  id: string
  vehiculo_id: string
  categoria_id: number
  plan_mantenimiento_id: string | null
  monto: number
  fecha: string
  kilometraje: number | null
  descripcion: string | null
}

/** Datos editables de un gasto (el gasto no cambia de vehículo). */
export interface GastoCambios {
  categoria_id: number
  plan_mantenimiento_id: string | null
  monto: number
  fecha: string
  kilometraje: number | null
  descripcion: string | null
}

export interface GastoNuevo extends GastoCambios {
  vehiculo_id: string
}
