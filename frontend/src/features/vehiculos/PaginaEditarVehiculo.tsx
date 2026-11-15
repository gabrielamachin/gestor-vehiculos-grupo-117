import { useNavigate, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { PaginaFormulario } from '../../shared/componentes/PaginaFormulario'
import { ConVehiculo } from './ConVehiculo'
import { FormularioAlias } from './FormularioAlias'

function ContenidoEditarVehiculo({ id }: { id: string }) {
  const navigate = useNavigate()
  const volver = `/vehiculos/${id}`

  return (
    <ConVehiculo id={id}>
      {(vehiculo) => (
        <PaginaFormulario volverA={volver} textoVolver={vehiculo.alias} titulo="Editar vehículo">
          <FormularioAlias vehiculo={vehiculo} alGuardar={() => navigate(volver)} />
        </PaginaFormulario>
      )}
    </ConVehiculo>
  )
}

export function PaginaEditarVehiculo() {
  const { id } = useParams<{ id: string }>()
  if (id === undefined) return <NoEncontrada />
  return <ContenidoEditarVehiculo key={id} id={id} />
}
