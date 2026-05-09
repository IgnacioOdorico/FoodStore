import { useAuthStore } from "../../../store/useAuthStore";

export const ForbiddenPage = () => {
  const { user } = useAuthStore();
  return (
    <div>
      <h1>403 - SIN ACCESO</h1>
      <p>
        Tu rol <strong>{user?.role}</strong> no tiene acceso a esta sección
      </p>
      <button onClick={() => window.history.back()}>Volver</button>
    </div>
  );
};
