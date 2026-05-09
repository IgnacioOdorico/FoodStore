export interface Categoria {
  id?: number;
  nombre: string;
  descripcion?: string;
  imagen_url?: string;
  parent_id?: number | null;
  
  // Auditoría
  created_at?: string;
  updated_at?: string;
  deleted_at?: string | null;

  // UI helpers
  children?: Categoria[];
}
