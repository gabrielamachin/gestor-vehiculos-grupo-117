import { Route, Routes } from 'react-router-dom'
import { PaginaLogin } from '../features/usuarios/PaginaLogin'
import { PaginaRegistro } from '../features/usuarios/PaginaRegistro'
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
          {/* Próximas pantallas: /vehiculos/:id, /gastos, /kilometraje, /mantenimiento, dashboard */}
        </Route>
      </Route>

      <Route path="*" element={<NoEncontrada />} />
    </Routes>
  )
}
