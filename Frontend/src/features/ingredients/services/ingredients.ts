import { apiFetch } from '../../../shared/services/api';
import type { Ingrediente } from '../types/ingrediente';

export const ingredientsService = {
  getAll: () => apiFetch('/ingredientes/'),
  getById: (id: number) => apiFetch(`/ingredientes/${id}`),
  create: (data: Partial<Ingrediente>) => apiFetch('/ingredientes/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Partial<Ingrediente>) => apiFetch(`/ingredientes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (id: number) => apiFetch(`/ingredientes/${id}`, { method: 'DELETE' }),
};
