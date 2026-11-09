import { useNavigate } from 'react-router-dom'
import { PaginaFormulario } from '../../shared/componentes/PaginaFormulario'
import { FormularioVehiculo } from './FormularioVehiculo'

export function PaginaNuevoVehiculo() {
  const navigate = useNavigate()
  return (
    <PaginaFormulario volverA="/" textoVolver="Mis vehículos" titulo="Agregar vehículo">
      <FormularioVehiculo alCrear={(vehiculo) => navigate(`/vehiculos/${vehiculo.id}`)} />
    </PaginaFormulario>
  )
}
