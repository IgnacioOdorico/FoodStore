import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { LayoutDashboard, ShoppingBasket, UtensilsCrossed } from 'lucide-react';
import logoProducts from '../assets/logo.png';
import logoCategories from '../assets/logo2.png';
import logoIngredients from '../assets/logo3.png';

export const Navbar: React.FC = () => {
  const location = useLocation();

  // Función para determinar qué logo mostrar y qué tamaño aplicar.
  // Productos e Ingredientes son "GIGANTES" y sobresalen del Navbar (h-32).
  const getLogoData = () => {
    if (location.pathname === '/products') return { src: logoProducts, size: 'w-48 h-48' };
    if (location.pathname === '/categories') return { src: logoCategories, size: 'w-32 h-32' };
    if (location.pathname === '/ingredients') return { src: logoIngredients, size: 'w-48 h-48' };
    return { src: logoProducts, size: 'w-32 h-32' };
  };

  const { src, size } = getLogoData();

  return (
    <nav className="fixed top-0 left-0 right-0 z-40 bg-brand shadow-xl border-b-4 border-cocoa">
      <div className="container mx-auto px-4">
        {/* Navbar se queda en h-32 como pidió Nacho */}
        <div className="flex items-center justify-between h-32">
          
          {/* SECCIÓN DEL LOGO Y BRANDING */}
          <div className="flex items-center gap-4 group cursor-pointer h-32 relative">
            <img 
              src={src} 
              alt="Logo" 
              className={`${size} object-contain transition-transform duration-500 group-hover:scale-110 z-50`}
            />
            {/* El título ahora se oculta en móviles (hidden md:flex) para dar prioridad a los links */}
            <div className="hidden md:flex flex-col">
              <span className="text-4xl font-black text-white tracking-tighter uppercase italic leading-none">
                Nacho Pizza Club
              </span>
            </div>
          </div>

          {/* MENÚ DE NAVEGACIÓN - Ahora SIEMPRE visible para permitir navegación en móviles */}
          <div className="flex items-center gap-1 md:gap-2 p-1 bg-black/10 rounded-2xl border-2 border-white/5 backdrop-blur-md">
            <NavItem to="/products" icon={<ShoppingBasket className="w-4 h-4" />} label="Productos" />
            <NavItem to="/categories" icon={<LayoutDashboard className="w-4 h-4" />} label="Categorías" />
            <NavItem to="/ingredients" icon={<UtensilsCrossed className="w-4 h-4" />} label="Ingredientes" />
          </div>
        </div>
      </div>
    </nav>
  );
};

// COMPONENTE INTERNO
const NavItem: React.FC<{ to: string; icon: React.ReactNode; label: string }> = ({ to, icon, label }) => (
  <NavLink
    to={to}
    className={({ isActive }) => `
      flex items-center gap-2 px-6 py-3 rounded-xl font-black uppercase italic tracking-widest text-[10px] transition-all duration-300
      ${isActive 
        ? 'bg-white text-brand shadow-lg scale-105' 
        : 'text-white/60 hover:text-white hover:bg-white/5'}
    `}
  >
    {icon}
    {label}
  </NavLink>
);
