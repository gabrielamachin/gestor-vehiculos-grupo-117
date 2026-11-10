import { Route, Routes } from 'react-router-dom'
import { PaginaEditarGasto } from '../features/gastos/PaginaEditarGasto'
import { PaginaNuevoGasto } from '../features/gastos/PaginaNuevoGasto'
import { PaginaEditarLectura } from '../features/kilometraje/PaginaEditarLectura'
import { PaginaNuevaLectura } from '../features/kilometraje/PaginaNuevaLectura'
import { PaginaEditarPlan } from '../features/mantenimiento/PaginaEditarPlan'
import { PaginaNuevoPlan } from '../features/mantenimiento/PaginaNuevoPlan'
import { PaginaLogin } from '../features/usuarios/PaginaLogin'
import { PaginaRegistro } from '../features/usuarios/PaginaRegistro'
import { PaginaNuevoVehiculo } from '../features/vehiculos/PaginaNuevoVehiculo'
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
          <Route path="vehiculos/nuevo" element={<PaginaNuevoVehiculo />} />
          <Route path="vehiculos/:id" element={<PaginaVehiculo />} />
          <Route path="vehiculos/:id/gastos/nuevo" element={<PaginaNuevoGasto />} />
          <Route path="gastos/:gastoId/editar" element={<PaginaEditarGasto />} />
          <Route path="vehiculos/:id/kilometraje/nuevo" element={<PaginaNuevaLectura />} />
          <Route path="kilometraje/:lecturaId/editar" element={<PaginaEditarLectura />} />
          <Route path="vehiculos/:id/planes/nuevo" element={<PaginaNuevoPlan />} />
          <Route path="planes/:planId/editar" element={<PaginaEditarPlan />} />
        </Route>
      </Route>

      <Route path="*" element={<NoEncontrada />} />
    </Routes>
  )
}
