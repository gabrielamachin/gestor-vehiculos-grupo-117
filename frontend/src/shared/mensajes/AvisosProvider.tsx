import { useCallback, useMemo, useRef, useState } from 'react'
import type { ReactNode } from 'react'
import { AvisosContext } from './avisos-context'
import type { Avisos } from './avisos-context'

type Tipo = 'exito' | 'error'

interface Aviso {
  id: number
  tipo: Tipo
  texto: string
}

const DURACION_MS = 4000

const ESTILOS: Record<Tipo, string> = {
  exito: 'border-emerald-200 bg-emerald-50 text-emerald-800',
  error: 'border-red-200 bg-red-50 text-red-700',
}

/**
 * Provee `useAvisos()` y muestra los avisos abajo, arriba de la barra del sistema del celular.
 * Vive en la raíz de la aplicación, por eso un aviso sigue visible aunque la pantalla que lo generó se cierre.
 */
export function AvisosProvider({ children }: { children: ReactNode }) {
  const [avisos, setAvisos] = useState<Aviso[]>([])
  const contador = useRef(0)

  const quitar = useCallback((id: number) => {
    setAvisos((actuales) => actuales.filter((a) => a.id !== id))
  }, [])

  const mostrar = useCallback(
    (tipo: Tipo, texto: string) => {
      contador.current += 1
      const id = contador.current
      // Varias solicitudes que fallan a la vez no deben apilar el mismo mensaje
      setAvisos((actuales) =>
        actuales.some((a) => a.tipo === tipo && a.texto === texto) ? actuales : [...actuales, { id, tipo, texto }],
      )
      window.setTimeout(() => quitar(id), DURACION_MS)
    },
    [quitar],
  )

  const valor = useMemo<Avisos>(
    () => ({ exito: (texto) => mostrar('exito', texto), error: (texto) => mostrar('error', texto) }),
    [mostrar],
  )

  return (
    <AvisosContext.Provider value={valor}>
      {children}
      <div
        aria-live="polite"
        className="pointer-events-none fixed inset-x-0 bottom-0 z-50 flex flex-col items-center gap-2 px-4 pb-[max(1rem,env(safe-area-inset-bottom))]"
      >
        {avisos.map((aviso) => (
          <div
            key={aviso.id}
            role={aviso.tipo === 'error' ? 'alert' : 'status'}
            className={`pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-xl border px-4 py-3 text-sm shadow-lg ${ESTILOS[aviso.tipo]}`}
          >
            <p className="flex-1">{aviso.texto}</p>
            <button
              type="button"
              onClick={() => quitar(aviso.id)}
              aria-label="Cerrar aviso"
              className="-mr-1 shrink-0 rounded px-1 text-lg leading-none opacity-60 transition hover:opacity-100"
            >
              ×
            </button>
          </div>
        ))}
      </div>
    </AvisosContext.Provider>
  )
}
