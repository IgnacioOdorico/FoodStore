import React from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
}

/**
 * ESTO ES UN COMPONENTE REUTILIZABLE: Lo creamos para no tener que 
 * copiar y pegar el código del fondo oscuro y el encabezado en cada modal.
 * Así mantengo la consistencia visual en toda la app.
 */
export const Modal: React.FC<ModalProps> = ({ 
  isOpen, 
  onClose, 
  title, 
  children,
  maxWidth = 'md' 
}) => {
  // Si el modal no está abierto, no renderizo NADA.
  if (!isOpen) return null;

  // Clases dinámicas para manejar distintos anchos (el de productos es más ancho que el de categorías)
  const maxWidthClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
  };

  return (
    // 'fixed inset-0' ocupa toda la pantalla y el z-50 lo pone por encima de todo.
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* OVERLAY: Es el fondo oscuro con el efecto de blur. Al hacer click, se cierra el modal. */}
      <div 
        className="absolute inset-0 bg-gray-900/60 backdrop-blur-sm animate-in fade-in duration-200" 
        onClick={onClose} 
      />
      
      {/* CONTENEDOR: El 'card' principal con sombra y bordes Cocoa. */}
      <div className={`relative card w-full ${maxWidthClasses[maxWidth]} animate-in fade-in zoom-in duration-200 shadow-2xl border-2 border-cocoa/20 max-h-[90vh] flex flex-col !p-0`}>
        
        {/* HEADER: Color Cocoa Brown con tipografía Black/Italic. Es el sello del branding. */}
        <div className="flex justify-between items-center p-6 bg-cocoa border-b-2 border-cocoa/20 rounded-t-2xl sticky top-0 z-10">
          <h2 className="text-xl font-black text-white uppercase tracking-tighter italic">
            {title}
          </h2>
          <button 
            onClick={onClose} 
            className="text-white/40 hover:text-white transition-colors p-1 hover:bg-white/10 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* CONTENIDO: Con scroll interno para que el modal no se escape si el formulario es muy largo. */}
        <div className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-cocoa/20 scrollbar-track-transparent">
          {children}
        </div>
      </div>
    </div>
  );
};
