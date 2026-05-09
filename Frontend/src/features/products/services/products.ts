import { apiFetch } from '../../../shared/services/api';
import type { Producto } from '../types/producto';

export const productsService = {
  getAll: () => apiFetch('/productos/'),
  getById: (id: number) => apiFetch(`/productos/${id}`),
  create: (data: Partial<Producto>) => apiFetch('/productos/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<Producto>) => apiFetch(`/productos/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => apiFetch(`/productos/${id}`, { method: 'DELETE' }),
};
