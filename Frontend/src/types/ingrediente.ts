export interface Ingrediente {
  id?: number;
  nombre: string;
  descripcion?: string;
  es_alergeno: boolean;
  
  created_at?: string;
  updated_at?: string;

  // Extra info from link table
  es_removible?: boolean;
}
