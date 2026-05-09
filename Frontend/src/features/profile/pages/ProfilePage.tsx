import { useAuthStore } from "../../../store/useAuthStore";

export const ProfilePage = () => {
  const { user } = useAuthStore();
  return (
    <div>
      <h1>Perfil</h1>
      <p>Nombre: {user?.name}</p>
      <p>Email: {user?.email}</p>
      <p>Rol: {user?.role}</p>
    </div>
  );
};
