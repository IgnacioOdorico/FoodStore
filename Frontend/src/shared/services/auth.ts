const BASE_URL = 'http://localhost:8000';

export type BackendUser = {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  roles: string[];
};

export function mapBackendRolesToFrontendRole(roles: string[]) {
  const normalizedRoles = roles.map((role) => role.toUpperCase());

  if (normalizedRoles.includes('ADMIN')) return 'admin';
  if (normalizedRoles.includes('STOCK') || normalizedRoles.includes('PEDIDOS')) return 'employee';
  return 'client';
}

function mapBackendUserToFrontendUser(user: BackendUser) {
  return {
    id: user.id,
    name: `${user.nombre} ${user.apellido}`,
    email: user.email,
    role: mapBackendRolesToFrontendRole(user.roles),
  };
}

async function readBackendUser(): Promise<BackendUser | null> {
  const response = await fetch(`${BASE_URL}/api/v1/auth/me`, {
    credentials: 'include',
  });

  if (response.status === 401) return null;
  if (!response.ok) throw new Error('No se pudo obtener la sesión actual');

  return response.json();
}

export async function loginWithBackend(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.set('username', email);
  formData.set('password', password);

  const response = await fetch(`${BASE_URL}/api/v1/auth/token`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Credenciales incorrectas');
  }

  const backendUser = await readBackendUser();
  return backendUser ? mapBackendUserToFrontendUser(backendUser) : null;
}

export async function getCurrentBackendUser() {
  const backendUser = await readBackendUser();
  return backendUser ? mapBackendUserToFrontendUser(backendUser) : null;
}

export async function logoutFromBackend() {
  await fetch(`${BASE_URL}/api/v1/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  }).catch(() => undefined);
}