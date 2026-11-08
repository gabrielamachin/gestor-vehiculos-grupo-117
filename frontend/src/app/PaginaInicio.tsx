import { ListaVehiculos } from '../features/vehiculos/ListaVehiculos'

export function PaginaInicio() {
  return (
    <section>
      <h1 className="mb-4 text-xl font-semibold">Mis vehículos</h1>
      <ListaVehiculos />
    </section>
  )
}
