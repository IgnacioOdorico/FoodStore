import { create } from "zustand";
import type { IRole, IUser } from "../shared/types/auth.types";

// MOCK — reemplazar por llamada real a /api/v1/auth/token cuando se integre el backend
const MOCK_USERS: Record<string, IUser> = {
  "admin@app.com": {
    id: 1,
    name: "Ana Admin",
    email: "admin@app.com",
    role: "admin",
  },
  "emp@app.com": {
    id: 2,
    name: "Eduardo Emp",
    email: "emp@app.com",
    role: "employee",
  },
  "client@app.com": {
    id: 3,
    name: "Carlos Client",
    email: "client@app.com",
    role: "client",
  },
};

interface AuthState {
  user: IUser | null;
  login: (email: string) => IUser | null;
  logout: VoidFunction;
  hasRole: (...roles: IRole[]) => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  login: (email) => {
    const found = MOCK_USERS[email];
    if (!found) return null;
    set({ user: found });
    return found;
  },
  logout: () => {
    set({ user: null });
  },
  hasRole: (...roles) => {
    const { user } = get();
    const found = user !== null && roles.includes(user.role);
    return found;
  },
}));
