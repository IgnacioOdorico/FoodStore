import React from 'react';

// Lo mismo que el botón: heredo todo del <input> nativo de HTML.
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string; // Puse esto para mostrar mensajes de validación debajo del input.
}

export const Input: React.FC<InputProps> = ({ label, error, className = '', ...props }) => {
  return (
    <div className="flex flex-col gap-1.5 w-full">
      {/* LABEL: Usamos tipografía Black e Itálica con color Cocoa para que se vea artesanal. */}
      <label className="text-sm font-black text-cocoa uppercase tracking-widest italic">
        {label}
      </label>
      
      <input
        {...props}
        // 'input-field' es la clase global que creamos en index.css para unificar el look.
        className={`input-field ${error ? 'border-red-500 bg-red-500/5' : ''} ${className}`}
      />
      
      {/* ERROR: Si hay un error, lo muestro en rojo bien llamativo. */}
      {error && (
        <span className="text-[10px] text-red-500 font-black uppercase tracking-tighter italic animate-in slide-in-from-top-1">
          {error}
        </span>
      )}
    </div>
  );
};
