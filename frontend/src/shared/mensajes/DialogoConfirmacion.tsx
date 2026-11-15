import { useEffect, useId, useRef, useState } from 'react'
import type { ChangeEvent, FormEvent, MouseEvent, SyntheticEvent } from 'react'
import type { OpcionesConfirmacion } from './confirmacion-context'

interface Props extends OpcionesConfirmacion {
  abierto: boolean
  /** Cambia con cada solicitud: así el texto escrito en una confirmación no pasa a la siguiente. */
  idSolicitud: number
  alResponder: (confirmado: boolean) => void
}

const normalizar = (texto: string) => texto.trim().toLowerCase()

/**
 * Diálogo modal basado en el elemento nativo <dialog>: el navegador se ocupa de mantener el foco dentro,
 * de la tecla Esc y de oscurecer el fondo, y los lectores de pantalla lo anuncian como diálogo.
 */
export function DialogoConfirmacion({ abierto, idSolicitud, alResponder, ...contenido }: Props) {
  const ref = useRef<HTMLDialogElement>(null)
  const idTitulo = useId()
  const idMensaje = useId()

  useEffect(() => {
    const dialogo = ref.current
    if (dialogo === null) return
    if (abierto && !dialogo.open) dialogo.showModal()
    if (!abierto && dialogo.open) dialogo.close()
  }, [abierto])

  // Esc: se evita el cierre nativo y se deja que lo decida el estado de la aplicación.
  function alCancelar(evento: SyntheticEvent<HTMLDialogElement>) {
    evento.preventDefault()
    alResponder(false)
  }

  // Un clic en el fondo oscuro llega con el propio <dialog> como destino (el contenido ocupa todo el interior).
  function alHacerClic(evento: MouseEvent<HTMLDialogElement>) {
    if (evento.target === evento.currentTarget) alResponder(false)
  }

  return (
    <dialog
      ref={ref}
      aria-labelledby={idTitulo}
      aria-describedby={idMensaje}
      onCancel={alCancelar}
      onClick={alHacerClic}
      className="m-auto w-[calc(100%-2rem)] max-w-sm rounded-2xl bg-white p-0 text-slate-900 shadow-xl backdrop:bg-slate-900/50"
    >
      <ContenidoDialogo key={idSolicitud} {...contenido} idTitulo={idTitulo} idMensaje={idMensaje} alResponder={alResponder} />
    </dialog>
  )
}

interface PropsContenido extends OpcionesConfirmacion {
  idTitulo: string
  idMensaje: string
  alResponder: (confirmado: boolean) => void
}

function ContenidoDialogo({
  titulo,
  mensaje,
  textoConfirmar = 'Confirmar',
  peligro = false,
  escribir,
  idTitulo,
  idMensaje,
  alResponder,
}: PropsContenido) {
  const [texto, setTexto] = useState('')
  const idCampo = useId()
  const habilitado = escribir === undefined || normalizar(texto) === normalizar(escribir)

  // Enter en el campo de texto confirma, pero solo si ya se escribió lo pedido
  function alEnviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    if (habilitado) alResponder(true)
  }

  const estiloConfirmar = peligro ? 'bg-red-600 text-white hover:bg-red-700' : 'bg-brand text-white hover:bg-brand/90'

  return (
    <form onSubmit={alEnviar} className="p-6">
      <h2 id={idTitulo} className="text-lg font-semibold">
        {titulo}
      </h2>
      <p id={idMensaje} className="mt-2 text-sm text-slate-600">
        {mensaje}
      </p>

      {escribir !== undefined && (
        <div className="mt-4 space-y-1">
          <label htmlFor={idCampo} className="block text-sm font-medium text-slate-700">
            Para confirmar, escribí <span className="font-semibold text-slate-900">{escribir}</span>
          </label>
          <input
            id={idCampo}
            value={texto}
            onChange={(evento: ChangeEvent<HTMLInputElement>) => setTexto(evento.target.value)}
            autoComplete="off"
            autoCapitalize="off"
            spellCheck={false}
            className="block min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3 text-base text-slate-900 focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand/20"
          />
        </div>
      )}

      {/* Cancelar va primero en el DOM: es el primer botón al tabular (lo más seguro en acciones destructivas).
          flex-col-reverse lo muestra debajo en el celular; en pantallas anchas queda a la izquierda. */}
      <div className="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
        <button
          type="button"
          onClick={() => alResponder(false)}
          className="inline-flex min-h-11 items-center justify-center rounded-lg border border-slate-300 bg-white px-4 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={!habilitado}
          className={`inline-flex min-h-11 items-center justify-center rounded-lg px-4 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50 ${estiloConfirmar}`}
        >
          {textoConfirmar}
        </button>
      </div>
    </form>
  )
}
