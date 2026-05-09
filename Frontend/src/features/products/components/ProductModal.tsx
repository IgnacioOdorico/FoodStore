import React, { useEffect } from 'react';
import { useForm } from '@tanstack/react-form';
import type { Producto } from '../types/producto';
import { Button } from '../../../shared/ui/Button';
import { Input } from '../../../shared/ui/Input';
import { Modal } from '../../../shared/ui/Modal';

import type { Categoria } from '../../categories/types/categoria';
import type { Ingrediente } from '../../ingredients/types/ingrediente';

interface ProductModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: Partial<Producto>) => void;
  productoSelected: Producto | null;
  categorias: Categoria[];
  ingredientes: Ingrediente[];
  isLoading?: boolean;
}

export const ProductModal: React.FC<ProductModalProps> = ({ 
  isOpen, 
  onClose, 
  onSave, 
  productoSelected,
  categorias,
  ingredientes,
  isLoading 
}) => {
  const form = useForm({
    defaultValues: {
      nombre: productoSelected?.nombre ?? '',
      descripcion: productoSelected?.descripcion ?? '',
      precio_base: productoSelected?.precio_base ?? 0,
      imagenes_url: productoSelected?.imagenes_url?.[0] ?? '',
      stock_cantidad: productoSelected?.stock_cantidad ?? 0,
      disponible: productoSelected?.disponible ?? true,
      categoria_ids: productoSelected?.categorias?.map(c => c.id!) ?? [],
      ingrediente_ids: productoSelected?.ingredientes?.map(i => i.id!) ?? [],
    },
    onSubmit: async ({ value }) => {
      onSave({
        ...value,
        imagenes_url: [value.imagenes_url],
        precio_base: Number(value.precio_base),
        stock_cantidad: Number(value.stock_cantidad)
      } as Partial<Producto>);
    },
  });

  useEffect(() => {
    if (isOpen) {
      form.reset({
        nombre: productoSelected?.nombre ?? '',
        descripcion: productoSelected?.descripcion ?? '',
        precio_base: productoSelected?.precio_base ?? 0,
        imagenes_url: productoSelected?.imagenes_url?.[0] ?? '',
        stock_cantidad: productoSelected?.stock_cantidad ?? 0,
        disponible: productoSelected?.disponible ?? true,
        categoria_ids: productoSelected?.categorias?.map(c => c.id!) ?? [],
        ingrediente_ids: productoSelected?.ingredientes?.map(i => i.id!) ?? [],
      });
    }
  }, [productoSelected, isOpen, form]);

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={productoSelected ? 'Editar Producto' : 'Nuevo Producto'}
      maxWidth="2xl"
    >
      <form 
        onSubmit={(e) => {
          e.preventDefault();
          e.stopPropagation();
          form.handleSubmit();
        }}
        className="flex flex-col gap-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <form.Field
            name="nombre"
            validators={{ onChange: ({ value }) => !value ? 'Requerido' : undefined }}
            children={(field) => (
              <Input label="Nombre" value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} error={field.state.meta.errors?.[0]?.toString()} />
            )}
          />

          <form.Field
            name="precio_base"
            validators={{ onChange: ({ value }) => value <= 0 ? 'Debe ser mayor a 0' : undefined }}
            children={(field) => (
              <Input label="Precio" type="number" value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(Number(e.target.value))} error={field.state.meta.errors?.[0]?.toString()} />
            )}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <form.Field
            name="imagenes_url"
            children={(field) => (
              <Input label="URL de Imagen" value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} />
            )}
          />
          <form.Field
            name="stock_cantidad"
            children={(field) => (
              <Input label="Stock Actual" type="number" value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(Number(e.target.value))} />
            )}
          />
        </div>

        <form.Field
          name="descripcion"
          children={(field) => (
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-black text-cocoa uppercase tracking-widest italic">Descripción</label>
              <textarea className="input-field min-h-[60px]" value={field.state.value} onBlur={field.handleBlur} onChange={(e) => field.handleChange(e.target.value)} />
            </div>
          )}
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Categorías Multi-select */}
          <form.Field
            name="categoria_ids"
            validators={{
              onChange: ({ value }) => !value || value.length === 0 ? 'Debe seleccionar al menos una categoría' : undefined
            }}
            children={(field) => (
              <div className="flex flex-col gap-1.5">
                <div className="flex justify-between items-center">
                  <label className="text-sm font-black text-cocoa uppercase tracking-widest italic">Categorías</label>
                  {field.state.meta.errors?.[0] && (
                    <span className="text-[9px] text-red-400 font-black uppercase tracking-tighter">{field.state.meta.errors[0].toString()}</span>
                  )}
                </div>
                <div className={`flex flex-wrap gap-2 p-3 bg-canvas/30 rounded-xl border-2 min-h-[100px] shadow-inner ${field.state.meta.errors?.[0] ? 'border-red-500/30' : 'border-cocoa/20'}`}>
                  {categorias.map(cat => (
                    <label key={cat.id} className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border-2 cursor-pointer transition-all ${field.state.value.includes(cat.id!) ? 'bg-brand text-white border-brand shadow-md scale-105' : 'bg-canvas/50 text-brand-active/70 border-cocoa/10 hover:border-cocoa/40'}`}>
                      <input
                        type="checkbox"
                        className="hidden"
                        checked={field.state.value.includes(cat.id!)}
                        onChange={(e) => {
                          const val = e.target.checked 
                            ? [...field.state.value, cat.id!]
                            : field.state.value.filter(id => id !== cat.id);
                          field.handleChange(val);
                        }}
                      />
                      <span className="text-[10px] font-black uppercase tracking-tighter italic">{cat.nombre}</span>
                    </label>
                  ))}
                </div>
              </div>
            )}
          />

          {/* Ingredientes Multi-select */}
          <form.Field
            name="ingrediente_ids"
            children={(field) => (
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-black text-cocoa uppercase tracking-widest italic">Ingredientes</label>
                <div className="flex flex-wrap gap-2 p-3 bg-canvas/30 rounded-xl border-2 border-cocoa/20 min-h-[100px] shadow-inner">
                  {ingredientes.map(ing => (
                    <label key={ing.id} className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border-2 cursor-pointer transition-all ${field.state.value.includes(ing.id!) ? 'bg-cocoa text-white border-cocoa shadow-md scale-105' : 'bg-canvas/50 text-brand-active/70 border-cocoa/10 hover:border-cocoa/40'}`}>
                      <input
                        type="checkbox"
                        className="hidden"
                        checked={field.state.value.includes(ing.id!)}
                        onChange={(e) => {
                          const val = e.target.checked 
                            ? [...field.state.value, ing.id!]
                            : field.state.value.filter(id => id !== ing.id);
                          field.handleChange(val);
                        }}
                      />
                      <span className="text-[10px] font-black uppercase tracking-tighter italic">{ing.nombre}</span>
                    </label>
                  ))}
                </div>
              </div>
            )}
          />
        </div>

        <form.Field
          name="disponible"
          children={(field) => (
            <label className="flex items-center gap-3 cursor-pointer w-fit p-3 bg-brand/10 rounded-xl border-2 border-brand/20">
              <input type="checkbox" checked={field.state.value} onChange={(e) => field.handleChange(e.target.checked)} className="w-5 h-5 text-brand rounded border-2 border-brand/20 bg-white/10 focus:ring-brand cursor-pointer" />
              <span className="text-sm font-black text-brand-active uppercase tracking-widest italic">Producto habilitado para la venta</span>
            </label>
          )}
        />

        <div className="flex justify-end gap-3 mt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button type="submit" isLoading={isLoading}>{productoSelected ? 'Actualizar' : 'Crear'} Producto</Button>
        </div>
      </form>
    </Modal>
  );
};
