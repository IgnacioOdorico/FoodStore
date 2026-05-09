import React from 'react';
import { Loader2, AlertCircle, Inbox } from 'lucide-react';
import { Button } from './Button';

/**
 * ESTE ARCHIVO ES CLAVE: Acá guardo los estados de la pantalla.
 * Me sirve para que el usuario sepa qué está pasando (si carga, si falló o si no hay nada).
 */

export const LoadingState: React.FC = () => (
  <div className="flex flex-col items-center justify-center py-20 gap-4 animate-in fade-in duration-500">
    {/* El 'animate-spin' hace que el icono de Lucide gire infinitamente. */}
    <Loader2 className="w-12 h-12 text-brand animate-spin" />
    <p className="text-cocoa font-black uppercase italic tracking-widest text-sm">Cargando delicias...</p>
  </div>
);

export const ErrorState: React.FC<{ message?: string; onRetry?: () => void }> = ({ 
  message = "Hubo un error al conectar con el servidor.", 
  onRetry 
}) => (
  <div className="flex flex-col items-center justify-center py-20 gap-4 bg-red-500/5 rounded-3xl border-2 border-red-500/20">
    <AlertCircle className="w-16 h-16 text-red-500" />
    <div className="text-center">
      <h3 className="text-xl font-black text-red-600 uppercase italic">¡Ups! Algo salió mal</h3>
      <p className="text-red-400 font-bold italic text-sm">{message}</p>
    </div>
    {/* El botón de reintentar llama a 'refetch()' de TanStack Query. Muy útil. */}
    {onRetry && (
      <Button variant="danger" onClick={onRetry} className="mt-2">
        Reintentar conexión
      </Button>
    )}
  </div>
);

export const EmptyState: React.FC<{ message: string }> = ({ message }) => (
  <div className="flex flex-col items-center justify-center py-20 gap-4 bg-canvas/30 rounded-3xl border-2 border-cocoa/10 border-dashed">
    <Inbox className="w-16 h-16 text-cocoa/30" />
    <p className="text-cocoa/60 font-black uppercase italic tracking-widest text-sm">{message}</p>
  </div>
);
