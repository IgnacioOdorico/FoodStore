import { create } from "zustand";
import type { IRole, IUser } from "../shared/types/auth.types";
import {
  getCurrentBackendUser,
  loginWithBackend,
  logoutFromBackend,
} from "../shared/services/auth";

interface AuthState {
  user: IUser | null;
  sessionReady: boolean;
  hydrateSession: () => Promise<void>;
  login: (email: string, password: string) => Promise<IUser | null>;
  logout: () => Promise<void>;
  hasRole: (...roles: IRole[]) => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  sessionReady: false,
  hydrateSession: async () => {
    const currentUser = await getCurrentBackendUser().catch(() => null);
    set({ user: currentUser, sessionReady: true });
  },
  login: async (email, password) => {
    const authenticatedUser = await loginWithBackend(email, password);
    set({ user: authenticatedUser, sessionReady: true });
    return authenticatedUser;
  },
  logout: async () => {
    await logoutFromBackend();
    set({ user: null });
  },
  hasRole: (...roles) => {
    const { user } = get();
    const found = user !== null && roles.includes(user.role);
    return found;
  },
}));
