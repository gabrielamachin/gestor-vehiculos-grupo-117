import { useNavigate, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { PaginaFormulario } from '../../shared/componentes/PaginaFormulario'
import { ConVehiculo } from '../vehiculos/ConVehiculo'
import { FormularioLectura } from './FormularioLectura'

function ContenidoNuevaLectura({ id }: { id: string }) {
  const navigate = useNavigate()
  const volver = `/vehiculos/${id}`

  return (
    <ConVehiculo id={id}>
      {(vehiculo) => (
        <PaginaFormulario volverA={volver} textoVolver={vehiculo.alias} titulo="Cargar kilometraje" subtitulo={vehiculo.alias}>
          <FormularioLectura vehiculo={vehiculo} alGuardar={() => navigate(volver)} />
        </PaginaFormulario>
      )}
    </ConVehiculo>
  )
}

export function PaginaNuevaLectura() {
  const { id } = useParams<{ id: string }>()
  if (id === undefined) return <NoEncontrada />
  return <ContenidoNuevaLectura key={id} id={id} />
}
