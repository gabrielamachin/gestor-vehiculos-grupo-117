import { useCallback, useRef, useState } from 'react'
import type { ReactNode } from 'react'
import { ConfirmacionContext } from './confirmacion-context'
import type { Confirmar, OpcionesConfirmacion } from './confirmacion-context'
import { DialogoConfirmacion } from './DialogoConfirmacion'

interface Pendiente {
  id: number
  opciones: OpcionesConfirmacion
  resolver: (confirmado: boolean) => void
}

const SIN_OPCIONES: OpcionesConfirmacion = { titulo: '', mensaje: '' }

/** Provee `useConfirmar()` a toda la aplicación y renderiza un único diálogo compartido. */
export function ConfirmacionProvider({ children }: { children: ReactNode }) {
  const [pendiente, setPendiente] = useState<Pendiente | null>(null)
  const contador = useRef(0)

  const confirmar = useCallback<Confirmar>(
    (opciones) =>
      new Promise<boolean>((resolver) => {
        contador.current += 1
        setPendiente({ id: contador.current, opciones, resolver })
      }),
    [],
  )

  function responder(confirmado: boolean) {
    pendiente?.resolver(confirmado)
    setPendiente(null)
  }

  return (
    <ConfirmacionContext.Provider value={confirmar}>
      {children}
      <DialogoConfirmacion
        abierto={pendiente !== null}
        idSolicitud={pendiente?.id ?? 0}
        {...(pendiente?.opciones ?? SIN_OPCIONES)}
        alResponder={responder}
      />
    </ConfirmacionContext.Provider>
  )
}
