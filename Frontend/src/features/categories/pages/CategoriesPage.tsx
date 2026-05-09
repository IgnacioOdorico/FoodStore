import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { categoriesService } from '../services/categories';
import { CategoriaTable } from '../components/CategoriaTable';
import { CategoriaModal } from '../components/CategoriaModal';
import { LoadingState, ErrorState, EmptyState } from '../../../shared/ui/States';
import { Button } from '../../../shared/ui/Button';
import { Plus } from 'lucide-react';
import type { Categoria } from '../types/categoria';

export const CategoriesPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [modalOpen, setModalOpen] = useState(false);
  const [selected, setSelected] = useState<Categoria | null>(null);

  // Consultar categorías
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['categories'],
    queryFn: categoriesService.getAll,
  });

  // Mutación para Crear/Editar
  const saveMutation = useMutation({
    mutationFn: (data: Partial<Categoria>) => {
      return selected?.id
        ? categoriesService.update(selected.id, data)
        : categoriesService.create(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
      handleClose();
    },
  });

  // Mutación para Eliminar
  const deleteMutation = useMutation({
    mutationFn: (id: number) => categoriesService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
    },
    onError: (error) => {
      console.error('Error al borrar:', error);
      alert('Error al borrar: ' + error.message);
    }
  });

  const handleOpen = (categoria?: Categoria) => {
    setSelected(categoria || null);
    setModalOpen(true);
  };

  const handleClose = () => {
    setModalOpen(false);
    setSelected(null);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('¿Estás seguro de eliminar esta categoría?')) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="flex flex-col gap-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-brand tracking-tight">Categorías</h1>
          <p className="text-gray-500">Gestioná las categorías de tus productos</p>
        </div>
        <Button onClick={() => handleOpen()} className="gap-2">
          <Plus className="w-5 h-5" />
          Nueva Categoría
        </Button>
      </div>

      {isLoading ? (
        <LoadingState />
      ) : isError ? (
        <ErrorState onRetry={() => refetch()} />
      ) : data && data.length > 0 ? (
        <CategoriaTable
          data={data}
          onEdit={handleOpen}
          onDelete={handleDelete}
        />
      ) : (
        <EmptyState message="No hay categorías creadas aún" />
      )}

      <CategoriaModal
        isOpen={modalOpen}
        onClose={handleClose}
        categoriaSelected={selected}
        categorias={data || []}
        onSave={(val) => saveMutation.mutate(val)}
        isLoading={saveMutation.isPending}
      />
    </div>
  );
};
