import { useNavigate, useParams } from 'react-router-dom'
import { NoEncontrada } from '../../app/NoEncontrada'
import { PaginaFormulario } from '../../shared/componentes/PaginaFormulario'
import { ConVehiculo } from '../vehiculos/ConVehiculo'
import { FormularioGasto } from './FormularioGasto'

function ContenidoNuevoGasto({ id }: { id: string }) {
  const navigate = useNavigate()
  const volver = `/vehiculos/${id}`

  return (
    <ConVehiculo id={id}>
      {(vehiculo) => (
        <PaginaFormulario volverA={volver} textoVolver={vehiculo.alias} titulo="Cargar gasto" subtitulo={vehiculo.alias}>
          <FormularioGasto vehiculo={vehiculo} alGuardar={() => navigate(volver)} />
        </PaginaFormulario>
      )}
    </ConVehiculo>
  )
}

export function PaginaNuevoGasto() {
  const { id } = useParams<{ id: string }>()
  if (id === undefined) return <NoEncontrada />
  return <ContenidoNuevoGasto key={id} id={id} />
}
