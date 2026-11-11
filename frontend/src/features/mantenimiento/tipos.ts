export interface PlanMantenimiento {
  id: string
  vehiculo_id: string
  nombre: string
  intervalo_km: number
}

/** Datos editables de un plan (el plan no cambia de vehículo). */
export interface PlanCambios {
  nombre: string
  intervalo_km: number
}

export interface PlanNuevo extends PlanCambios {
  vehiculo_id: string
}
