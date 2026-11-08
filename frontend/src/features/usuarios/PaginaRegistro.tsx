import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { mensajeDeError } from '../../shared/api/errores'
import { Alerta } from '../../shared/componentes/Alerta'
import { Boton } from '../../shared/componentes/Boton'
import { Campo } from '../../shared/componentes/Campo'
import { TarjetaAuth } from '../../shared/componentes/TarjetaAuth'
import { useAuth } from './useAuth'

export function PaginaRegistro() {
  const { registrarse } = useAuth()
  const [nombre, setNombre] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmacion, setConfirmacion] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  // Primera capa de validación (la API valida de nuevo: ver docs/esquema-db.md, sección 6).
  function validar(): string | null {
    if (nombre.trim() === '') return 'Ingresá tu nombre.'
    if (password.length < 8) return 'La contraseña debe tener al menos 8 caracteres.'
    if (new TextEncoder().encode(password).length > 72) return 'La contraseña es demasiado larga (máximo 72 bytes).'
    if (password !== confirmacion) return 'Las contraseñas no coinciden.'
    return null
  }

  async function alEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    const problema = validar()
    if (problema !== null) {
      setError(problema)
      return
    }
    setError(null)
    setEnviando(true)
    try {
      await registrarse(nombre.trim(), email.trim(), password)
      // Con la sesión iniciada, RutaPublica redirige sola a la pantalla principal.
    } catch (e) {
      setError(mensajeDeError(e))
      setEnviando(false)
    }
  }

  return (
    <TarjetaAuth titulo="Crear cuenta" subtitulo="Registrá tus vehículos y conocé cuánto te cuesta cada kilómetro.">
      <form onSubmit={alEnviar} className="space-y-4">
        <Campo
          etiqueta="Nombre"
          nombre="nombre"
          autoComplete="name"
          required
          maxLength={150}
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
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
          autoComplete="new-password"
          required
          ayuda="Mínimo 8 caracteres."
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Campo
          etiqueta="Repetir contraseña"
          nombre="confirmacion"
          type="password"
          autoComplete="new-password"
          required
          value={confirmacion}
          onChange={(e) => setConfirmacion(e.target.value)}
        />
        {error && <Alerta>{error}</Alerta>}
        <Boton type="submit" cargando={enviando} className="w-full">
          Crear cuenta
        </Boton>
      </form>
      <p className="mt-5 text-center text-sm text-slate-600">
        ¿Ya tenés cuenta?{' '}
        <Link to="/login" className="font-medium text-brand hover:underline">
          Ingresá
        </Link>
      </p>
    </TarjetaAuth>
  )
}
