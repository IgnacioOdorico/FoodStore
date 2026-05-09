import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { productsService } from '../services/products';
import { ProductTable } from '../components/ProductTable';
import { ProductModal } from '../components/ProductModal';
import { LoadingState, ErrorState, EmptyState } from '../../../shared/ui/States';
import { Button } from '../../../shared/ui/Button';
import { Plus } from 'lucide-react';
import type { Producto } from '../types/producto';

import { categoriesService } from '../../categories/services/categories';
import { ingredientsService } from '../../ingredients/services/ingredients';

export const ProductsPage: React.FC = () => {
  // El queryClient me sirve para 'invalidar' la caché. 
  // O sea, avisarle a React que los datos cambiaron y tiene que volver a pedirlos.
  const queryClient = useQueryClient();
  
  // Estados locales para el modal y el producto seleccionado (para editar)
  const [modalOpen, setModalOpen] = useState(false);
  const [selected, setSelected] = useState<Producto | null>(null);

  // TANSTACK QUERY (useQuery): Esto reemplaza al viejo useEffect + fetch.
  // Me maneja automáticamente el estado de 'isLoading', 'isError' y la caché.
  const { data: products, isLoading, isError, refetch } = useQuery({
    queryKey: ['products'], // Esta es la "llave" de la caché
    queryFn: productsService.getAll,
  });

  // También traigo categorías e ingredientes para pasárselos al modal de creación
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: categoriesService.getAll,
  });

  const { data: ingredients } = useQuery({
    queryKey: ['ingredients'],
    queryFn: ingredientsService.getAll,
  });

  // MUTACIONES (useMutation): Esto lo uso para CREAR o EDITAR.
  // Lo bueno es que me permite definir qué hacer cuando la operación sale bien (onSuccess).
  const saveMutation = useMutation({
    mutationFn: (data: Partial<Producto>) => {
      return selected?.id 
        ? productsService.update(selected.id, data)
        : productsService.create(data);
    },
    onSuccess: () => {
      // ACÁ ESTÁ EL SECRETO: Invalido la query 'products' para que la tabla se refresque sola.
      queryClient.invalidateQueries({ queryKey: ['products'] });
      handleClose();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => productsService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });

  const handleOpen = (producto?: Producto) => {
    setSelected(producto || null);
    setModalOpen(true);
  };

  const handleClose = () => {
    setModalOpen(false);
    setSelected(null);
  };

  const handleDelete = (id: number) => {
    // Puse un confirm básico para que no se borre nada sin querer.
    if (window.confirm('¿Estás seguro de eliminar este producto?')) {
      deleteMutation.mutate(id);
    }
  };

  // MANEJO DE ESTADOS DE LA UI:
  // Si está cargando, muestro el spinner. Si falló, muestro el error.
  if (isLoading) return <LoadingState />;
  if (isError) return <ErrorState onRetry={() => refetch()} />;

  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <div>
          {/* Títulos con tipografía Black e Itálica para que se vea premium */}
          <h1 className="text-3xl font-black text-brand-active tracking-tighter uppercase italic">Productos</h1>
          <p className="text-cocoa font-bold italic text-sm opacity-80">Gestioná tu catálogo de productos</p>
        </div>
        <Button onClick={() => handleOpen()} className="gap-2">
          <Plus className="w-5 h-5" />
          Nuevo Producto
        </Button>
      </div>

      {/* Si hay productos, muestro la tabla. Si no, el EmptyState. */}
      {products && products.length > 0 ? (
        <ProductTable data={products} onEdit={handleOpen} onDelete={handleDelete} />
      ) : (
        <EmptyState message="No hay productos registrados" />
      )}

      {/* El Modal: Le paso todo por props. Es una forma de desacoplar la lógica. */}
      <ProductModal
        isOpen={modalOpen}
        onClose={handleClose}
        productoSelected={selected}
        categorias={categories || []}
        ingredientes={ingredients || []}
        onSave={(val) => saveMutation.mutate(val)}
        isLoading={saveMutation.isPending}
      />
    </div>
  );
};
