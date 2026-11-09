import { BotonEnlace } from '../shared/componentes/BotonEnlace'
import { ListaVehiculos } from '../features/vehiculos/ListaVehiculos'

export function PaginaInicio() {
  return (
    <section>
      <div className="mb-4 flex items-center justify-between gap-3">
        <h1 className="text-xl font-semibold">Mis vehículos</h1>
        <BotonEnlace to="/vehiculos/nuevo">+ Agregar</BotonEnlace>
      </div>
      <ListaVehiculos />
    </section>
  )
}
