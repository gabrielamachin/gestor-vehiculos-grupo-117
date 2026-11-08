export function Cargando({ mensaje = 'Cargando…' }: { mensaje?: string }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 text-center text-sm text-slate-600">
      <div>
        <p>{mensaje}</p>
        {/* La instancia gratuita de Render se "duerme" y la primera solicitud puede tardar */}
        <p className="mt-1 text-xs text-slate-400">La primera conexión puede tardar unos segundos.</p>
      </div>
    </div>
  )
}
