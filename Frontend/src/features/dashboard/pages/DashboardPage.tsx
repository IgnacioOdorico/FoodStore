import { useAuthStore } from "../../../store/useAuthStore";

export const DashboardPage = () => {
  const { user } = useAuthStore();
  return (
    <div>
      <h1>Dashboard</h1>
      <p>
        Bienvenido {user?.name} con rol: {user?.role}
      </p>
    </div>
  );
};
