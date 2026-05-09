import React from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, ShoppingBasket, UtensilsCrossed, Users, ShoppingCart, User, LogOut } from 'lucide-react';
import { useAuthStore } from '../../store/useAuthStore';

export const Navbar: React.FC = () => {
  const { user, logout, hasRole } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Si no hay usuario autenticado, no mostramos el Navbar
  if (!user) return null;

  return (
    <nav className="fixed top-0 left-0 right-0 z-40 bg-brand shadow-xl border-b-4 border-cocoa">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">

          {/* BRANDING */}
          <Link to="/dashboard" className="flex items-center gap-3">
            <span className="text-2xl font-black text-white tracking-tighter uppercase italic leading-none">
              FoodStore
            </span>
          </Link>

          {/* MENÚ SEGÚN ROL */}
          <div className="flex items-center gap-1 p-1 bg-black/10 rounded-2xl border-2 border-white/5 backdrop-blur-md">

            {/* admin + employee ven el catálogo */}
            {hasRole('admin', 'employee') && (
              <>
                <NavItem to="/dashboard"    icon={<LayoutDashboard className="w-4 h-4" />} label="Dashboard" />
                <NavItem to="/products"     icon={<ShoppingBasket className="w-4 h-4" />}  label="Productos" />
                <NavItem to="/categories"   icon={<LayoutDashboard className="w-4 h-4" />} label="Categorías" />
                <NavItem to="/ingredients"  icon={<UtensilsCrossed className="w-4 h-4" />} label="Ingredientes" />
              </>
            )}

            {/* solo admin ve gestión de usuarios */}
            {hasRole('admin') && (
              <NavItem to="/admin/users" icon={<Users className="w-4 h-4" />} label="Usuarios" />
            )}

            {/* client ve sus pedidos */}
            {hasRole('client') && (
              <NavItem to="/orders" icon={<ShoppingCart className="w-4 h-4" />} label="Mis Pedidos" />
            )}

            {/* cualquier autenticado ve perfil */}
            <NavItem to="/profile" icon={<User className="w-4 h-4" />} label="Perfil" />
          </div>

          {/* USUARIO + LOGOUT */}
          <div className="flex items-center gap-3">
            <span className="text-white/70 text-sm font-semibold">
              {user.name} <span className="text-white/40">({user.role})</span>
            </span>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1 px-3 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-bold uppercase tracking-wider transition-all duration-200"
            >
              <LogOut className="w-3 h-3" />
              Salir
            </button>
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
      flex items-center gap-2 px-4 py-2 rounded-xl font-black uppercase italic tracking-widest text-[10px] transition-all duration-300
      ${isActive
        ? 'bg-white text-brand shadow-lg scale-105'
        : 'text-white/60 hover:text-white hover:bg-white/5'}
    `}
  >
    {icon}
    {label}
  </NavLink>
);
