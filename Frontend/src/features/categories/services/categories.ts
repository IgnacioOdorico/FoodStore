import { apiFetch } from '../../../shared/services/api';
import type { Categoria } from '../types/categoria';

export const categoriesService = {
  getAll: () => apiFetch('/api/v1/categorias/'),
  getById: (id: number) => apiFetch(`/api/v1/categorias/${id}`),
  create: (data: Partial<Categoria>) => apiFetch('/api/v1/categorias/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<Categoria>) => apiFetch(`/api/v1/categorias/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => apiFetch(`/api/v1/categorias/${id}`, { method: 'DELETE' }),
};
