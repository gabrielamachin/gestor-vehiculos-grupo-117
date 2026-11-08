import { Link } from 'react-router-dom'

export function NoEncontrada() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-3 bg-slate-50 px-4 text-center">
      <p className="text-lg font-semibold text-slate-900">Esta página no existe</p>
      <Link to="/" className="text-sm font-medium text-brand hover:underline">
        Volver al inicio
      </Link>
    </div>
  )
}
