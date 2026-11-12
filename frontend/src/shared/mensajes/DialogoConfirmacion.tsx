import { useEffect, useId, useRef } from 'react'
import type { MouseEvent, SyntheticEvent } from 'react'
import type { OpcionesConfirmacion } from './confirmacion-context'

interface Props extends OpcionesConfirmacion {
  abierto: boolean
  alResponder: (confirmado: boolean) => void
}

/**
 * Diálogo modal basado en el elemento nativo <dialog>: el navegador se ocupa de mantener el foco dentro,
 * de la tecla Esc y de oscurecer el fondo, y los lectores de pantalla lo anuncian como diálogo.
 */
export function DialogoConfirmacion({ abierto, titulo, mensaje, textoConfirmar = 'Confirmar', peligro = false, alResponder }: Props) {
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

  // Un clic en el fondo oscuro llega con el propio <dialog> como destino (el contenido está dentro de un div con padding).
  function alHacerClic(evento: MouseEvent<HTMLDialogElement>) {
    if (evento.target === evento.currentTarget) alResponder(false)
  }

  const estiloConfirmar = peligro ? 'bg-red-600 text-white hover:bg-red-700' : 'bg-brand text-white hover:bg-brand/90'

  return (
    <dialog
      ref={ref}
      aria-labelledby={idTitulo}
      aria-describedby={idMensaje}
      onCancel={alCancelar}
      onClick={alHacerClic}
      className="m-auto w-[calc(100%-2rem)] max-w-sm rounded-2xl bg-white p-0 text-slate-900 shadow-xl backdrop:bg-slate-900/50"
    >
      <div className="p-6">
        <h2 id={idTitulo} className="text-lg font-semibold">
          {titulo}
        </h2>
        <p id={idMensaje} className="mt-2 text-sm text-slate-600">
          {mensaje}
        </p>
        {/* Cancelar va primero en el DOM: es el botón que recibe el foco al abrirse (lo más seguro en acciones destructivas).
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
            type="button"
            onClick={() => alResponder(true)}
            className={`inline-flex min-h-11 items-center justify-center rounded-lg px-4 text-sm font-medium transition ${estiloConfirmar}`}
          >
            {textoConfirmar}
          </button>
        </div>
      </div>
    </dialog>
  )
}
