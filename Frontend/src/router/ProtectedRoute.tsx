import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../store/useAuthStore";
import type { IRole } from "../shared/types/auth.types";

type Props = {
  allowedRoles: IRole[];
};

export const ProtectedRoute = ({ allowedRoles }: Props) => {
  const { user, hasRole } = useAuthStore();

  // si no inició sesión → al login
  if (!user) {
    return <Navigate to="/login" />;
  }
  // si no tiene el rol necesario → forbidden
  if (!hasRole(...allowedRoles)) {
    return <Navigate to="/forbidden" />;
  }
  // cumple → renderiza la ruta hija
  return <Outlet />;
};
