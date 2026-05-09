import { apiFetch } from '../../../shared/services/api';
import type { Categoria } from '../types/categoria';

export const categoriesService = {
  getAll: () => apiFetch('/categorias/'),
  getById: (id: number) => apiFetch(`/categorias/${id}`),
  create: (data: Partial<Categoria>) => apiFetch('/categorias/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<Categoria>) => apiFetch(`/categorias/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => apiFetch(`/categorias/${id}`, { method: 'DELETE' }),
};
