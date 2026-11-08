import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { Boton } from '../../shared/componentes/Boton'
import { Campo } from '../../shared/componentes/Campo'
import { TarjetaAuth } from '../../shared/componentes/TarjetaAuth'
import { useAuth } from './useAuth'

export function PaginaLogin() {
  const { iniciarSesion } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  async function alEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    setError(null)
    setEnviando(true)
    try {
      await iniciarSesion(email.trim(), password)
      // Con la sesión iniciada, RutaPublica redirige sola a la pantalla principal.
    } catch (e) {
      setError(mensajeDeError(e))
      setEnviando(false)
    }
  }

  return (
    <TarjetaAuth titulo="Iniciar sesión" subtitulo="Ingresá para ver los gastos de tus vehículos.">
      <form onSubmit={alEnviar} className="space-y-4">
        <Campo
          etiqueta="Email"
          nombre="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <Campo
          etiqueta="Contraseña"
          nombre="password"
          type="password"
          autoComplete="current-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <Alerta>{error}</Alerta>}
        <Boton type="submit" cargando={enviando} className="w-full">
          Ingresar
        </Boton>
      </form>
      <p className="mt-5 text-center text-sm text-slate-600">
        ¿No tenés cuenta?{' '}
        <Link to="/registro" className="font-medium text-brand hover:underline">
          Registrate
        </Link>
      </p>
    </TarjetaAuth>
  )
}
