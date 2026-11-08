import { Route, Routes } from 'react-router-dom'
import { PaginaLogin } from '../features/usuarios/PaginaLogin'
import { PaginaRegistro } from '../features/usuarios/PaginaRegistro'
import { PaginaVehiculo } from '../features/vehiculos/PaginaVehiculo'
import { Layout } from './Layout'
import { NoEncontrada } from './NoEncontrada'
import { PaginaInicio } from './PaginaInicio'
import { RutaProtegida } from './RutaProtegida'
import { RutaPublica } from './RutaPublica'

export default function App() {
  return (
    <Routes>
      <Route element={<RutaPublica />}>
        <Route path="/login" element={<PaginaLogin />} />
        <Route path="/registro" element={<PaginaRegistro />} />
      </Route>

      <Route element={<RutaProtegida />}>
        <Route element={<Layout />}>
          <Route index element={<PaginaInicio />} />
          <Route path="vehiculos/:id" element={<PaginaVehiculo />} />
          {/* Próximas pantallas: alta de vehículo, gastos, kilometraje y planes de mantenimiento */}
        </Route>
      </Route>

      <Route path="*" element={<NoEncontrada />} />
    </Routes>
  )
}
