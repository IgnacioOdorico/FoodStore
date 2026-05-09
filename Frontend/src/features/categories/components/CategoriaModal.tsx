import React, { useEffect } from 'react';
import { useForm } from '@tanstack/react-form';
import type { Categoria } from '../types/categoria';
import { Button } from '../../../shared/ui/Button';
import { Input } from '../../../shared/ui/Input';
import { Modal } from '../../../shared/ui/Modal';

interface CategoriaModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: Partial<Categoria>) => void;
  categoriaSelected: Categoria | null;
  categorias: Categoria[];
  isLoading?: boolean;
}

export const CategoriaModal: React.FC<CategoriaModalProps> = ({ 
  isOpen, 
  onClose, 
  onSave, 
  categoriaSelected,
  categorias,
  isLoading 
}) => {
  const form = useForm({
    defaultValues: {
      nombre: categoriaSelected?.nombre ?? '',
      descripcion: categoriaSelected?.descripcion ?? '',
      imagen_url: categoriaSelected?.imagen_url ?? '',
      parent_id: categoriaSelected?.parent_id ?? null,
    },
    onSubmit: async ({ value }) => {
      onSave(value as Partial<Categoria>);
    },
  });

  useEffect(() => {
    if (isOpen) {
      form.reset({
        nombre: categoriaSelected?.nombre ?? '',
        descripcion: categoriaSelected?.descripcion ?? '',
        imagen_url: categoriaSelected?.imagen_url ?? '',
        parent_id: categoriaSelected?.parent_id ?? null,
      });
    }
  }, [categoriaSelected, isOpen, form]);

  const possibleParents = categorias.filter(c => c.id !== categoriaSelected?.id);

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={categoriaSelected ? 'Editar Categoría' : 'Nueva Categoría'}
      maxWidth="md"
    >
      <form 
        onSubmit={(e) => {
          e.preventDefault();
          e.stopPropagation();
          form.handleSubmit();
        }}
        className="flex flex-col gap-4"
      >
        <form.Field
          name="nombre"
          validators={{
            onChange: ({ value }) => !value ? 'El nombre es obligatorio' : undefined
          }}
          children={(field) => (
            <Input
              label="Nombre"
              placeholder="Ej: Pizzas"
              value={field.state.value}
              onBlur={field.handleBlur}
              onChange={(e) => field.handleChange(e.target.value)}
              error={field.state.meta.errors?.[0]?.toString()}
            />
          )}
        />

        <form.Field
          name="imagen_url"
          children={(field) => (
            <Input
              label="URL de Imagen"
              placeholder="https://example.com/imagen.jpg"
              value={field.state.value}
              onBlur={field.handleBlur}
              onChange={(e) => field.handleChange(e.target.value)}
            />
          )}
        />

        <form.Field
          name="parent_id"
          children={(field) => (
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-black text-cocoa uppercase tracking-widest italic">Categoría Padre (Opcional)</label>
              <select
                className="input-field"
                value={field.state.value ?? ''}
                onChange={(e) => field.handleChange(e.target.value ? Number(e.target.value) : null)}
              >
                <option value="" className="bg-brand text-white">Ninguna (Raíz)</option>
                {possibleParents.map(c => (
                  <option key={c.id} value={c.id} className="bg-brand text-white">{c.nombre}</option>
                ))}
              </select>
            </div>
          )}
        />

        <form.Field
          name="descripcion"
          children={(field) => (
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-black text-cocoa uppercase tracking-widest italic">Descripción</label>
              <textarea
                className="input-field min-h-[80px]"
                placeholder="Describe la categoría..."
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
            </div>
          )}
        />

        <div className="flex justify-end gap-3 mt-4">
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancelar
          </Button>
          <Button type="submit" isLoading={isLoading}>
            {categoriaSelected ? 'Actualizar' : 'Crear'} Categoría
          </Button>
        </div>
      </form>
    </Modal>
  );
};
