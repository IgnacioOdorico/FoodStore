import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ingredientsService } from '../services/ingredients';
import { IngredientTable } from '../components/IngredientTable';
import { IngredientModal } from '../components/IngredientModal';
import { LoadingState, ErrorState, EmptyState } from '../../../shared/ui/States';
import { Button } from '../../../shared/ui/Button';
import { Plus } from 'lucide-react';
import type { Ingrediente } from '../types/ingrediente';

export const IngredientsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [modalOpen, setModalOpen] = useState(false);
  const [selected, setSelected] = useState<Ingrediente | null>(null);

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['ingredients'],
    queryFn: ingredientsService.getAll,
  });

  const saveMutation = useMutation({
    mutationFn: (data: Partial<Ingrediente>) => {
      return selected?.id 
        ? ingredientsService.update(selected.id, data)
        : ingredientsService.create(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredients'] });
      handleClose();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => ingredientsService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingredients'] });
    },
  });

  const handleOpen = (ingrediente?: Ingrediente) => {
    setSelected(ingrediente || null);
    setModalOpen(true);
  };

  const handleClose = () => {
    setModalOpen(false);
    setSelected(null);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('¿Estás seguro de eliminar este ingrediente?')) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="flex flex-col gap-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-brand tracking-tight">Ingredientes</h1>
          <p className="text-gray-500">Manejo de stock y materias primas</p>
        </div>
        <Button onClick={() => handleOpen()} className="gap-2">
          <Plus className="w-5 h-5" />
          Nuevo Ingrediente
        </Button>
      </div>

      {isLoading ? (
        <LoadingState />
      ) : isError ? (
        <ErrorState onRetry={() => refetch()} />
      ) : data && data.length > 0 ? (
        <IngredientTable data={data} onEdit={handleOpen} onDelete={handleDelete} />
      ) : (
        <EmptyState message="No hay ingredientes en stock" />
      )}

      <IngredientModal
        isOpen={modalOpen}
        onClose={handleClose}
        ingredientSelected={selected}
        onSave={(val) => saveMutation.mutate(val)}
        isLoading={saveMutation.isPending}
      />
    </div>
  );
};
