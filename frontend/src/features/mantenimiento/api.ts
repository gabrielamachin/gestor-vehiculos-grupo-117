import { solicitar } from '../../shared/api/cliente'
import type { PlanMantenimiento } from './tipos'

export function listarPlanes(vehiculoId: string): Promise<PlanMantenimiento[]> {
  return solicitar<PlanMantenimiento[]>('/mantenimiento', { params: { vehiculo_id: vehiculoId } })
}
