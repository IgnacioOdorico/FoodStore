const BASE_URL = 'http://localhost:8000';

// Función para simular retraso de red (útil para el video del parcial)
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // CLAVE UN DELAY DE 1.5 SEGUNDOS PARA QUE SE VEA EL LOADING EN EL VIDEO XDDDD
  await delay(1500);

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Error en la petición');
  }

  // En DELETE (204 No Content), response.json() falla.
  if (response.status === 204) return null;

  return response.json();
}
