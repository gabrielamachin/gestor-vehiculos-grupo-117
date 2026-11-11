import { useNavigate, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { PaginaFormulario } from '../../shared/componentes/PaginaFormulario'
import { ConVehiculo } from '../vehiculos/ConVehiculo'
import { FormularioPlan } from './FormularioPlan'

function ContenidoNuevoPlan({ id }: { id: string }) {
  const navigate = useNavigate()
  const volver = `/vehiculos/${id}`

  return (
    <ConVehiculo id={id}>
      {(vehiculo) => (
        <PaginaFormulario volverA={volver} textoVolver={vehiculo.alias} titulo="Agregar plan de mantenimiento" subtitulo={vehiculo.alias}>
          <FormularioPlan vehiculo={vehiculo} alGuardar={() => navigate(volver)} />
        </PaginaFormulario>
      )}
    </ConVehiculo>
  )
}

export function PaginaNuevoPlan() {
  const { id } = useParams<{ id: string }>()
  if (id === undefined) return <NoEncontrada />
  return <ContenidoNuevoPlan key={id} id={id} />
}
