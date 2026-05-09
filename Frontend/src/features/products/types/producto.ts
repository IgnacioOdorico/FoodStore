import { Categoria } from \"../../categories/types/categoria\";
import { Ingrediente } from \"../../ingredients/types/ingrediente\";

export interface Producto {
    id?: number;
    nombre: string;
    descripcion?: string;
    precio_base: number;
    imagenes_url: string[];
    stock_cantidad: number;
    disponible: boolean;
    
    created_at?: string;
    updated_at?: string;
    deleted_at?: string | null;

    // Relaciones
    categorias?: (Categoria & { es_principal?: boolean })[];
    ingredientes?: (Ingrediente & { es_removible?: boolean })[];
}
