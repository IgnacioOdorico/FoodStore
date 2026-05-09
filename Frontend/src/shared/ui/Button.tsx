import React from 'react';

// EXTENDS: Heredo todas las propiedades de un botón normal de HTML.
// Así no tengo que redefinir cosas como 'disabled', 'type' o 'onClick'.
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  isLoading?: boolean; // Le puse esto para mostrar el spinner cuando guardamos algo.
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'primary', 
  isLoading, 
  className = '', 
  type = 'button',
  onClick,
  ...props 
}) => {
  // Uso este mapeo para aplicar las clases que definí en el index.css.
  // Es mucho más limpio que meter 50 clases de Tailwind acá adentro.
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    danger: 'btn-danger'
  };

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    // Si el botón está cargando, bloqueo el click para que no manden 50 veces el formulario.
    if (isLoading) return;
    if (onClick) onClick(e);
  };

  return (
    <button 
      {...props}
      type={type}
      className={`${variants[variant]} ${className} flex items-center justify-center gap-2`}
      disabled={isLoading || props.disabled}
      onClick={handleClick}
    >
      {/* EL SPINNER: Solo se muestra si isLoading es true. Es puro feedback para el usuario. */}
      {isLoading && (
        <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
      )}
      {children}
    </button>
  );
};
