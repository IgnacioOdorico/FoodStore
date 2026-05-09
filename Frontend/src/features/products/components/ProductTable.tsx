import React from 'react';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import type { Producto } from '../types/producto';
import { Button } from '../../../shared/ui/Button';
import { Pencil, Trash2, CheckCircle, XCircle, Eye } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface ProductTableProps {
  data: Producto[];
  onEdit: (producto: Producto) => void;
  onDelete: (id: number) => void;
}

const columnHelper = createColumnHelper<Producto>();

export const ProductTable: React.FC<ProductTableProps> = ({ data, onEdit, onDelete }) => {
  const navigate = useNavigate();
  const columns = [
    columnHelper.accessor('nombre', {
      header: 'Producto',
      cell: info => (
        <div className="flex items-center gap-3">
          {info.row.original.imagenes_url?.[0] && (
            <img src={info.row.original.imagenes_url[0]} alt="" className="w-12 h-12 rounded-xl object-cover border-2 border-cocoa/20 shadow-sm" />
          )}
          <div className="flex flex-col">
            <span className="font-black text-white uppercase italic tracking-tighter">{info.getValue()}</span>
            <span className="text-[10px] text-white/50 line-clamp-1 italic">{info.row.original.descripcion}</span>
          </div>
        </div>
      ),
    }),
    columnHelper.display({
      id: 'relations',
      header: 'Categorías / Ingredientes',
      cell: info => (
        <div className="flex flex-col gap-1.5">
          <div className="flex flex-wrap gap-1">
            {info.row.original.categorias?.map(c => (
              <span key={c.id} className={`text-[9px] px-2 py-0.5 rounded-full font-black uppercase border ${c.es_principal ? 'bg-canvas text-brand-active border-cocoa/20' : 'bg-white/5 text-white/60 border-white/10'}`}>
                {c.nombre}
              </span>
            ))}
          </div>
          <div className="flex flex-wrap gap-1">
            {info.row.original.ingredientes?.map(i => (
              <span key={i.id} className={`text-[9px] px-2 py-0.5 rounded-full font-black uppercase border ${i.es_alergeno ? 'bg-red-500/20 text-red-300 border-red-500/30' : 'bg-orange-500/20 text-orange-300 border-orange-500/30'}`}>
                {i.nombre}
              </span>
            ))}
          </div>
        </div>
      ),
    }),
    columnHelper.accessor('precio_base', {
      header: 'Precio',
      cell: info => <span className="font-mono font-black text-lg text-white drop-shadow-sm">${Number(info.getValue()).toLocaleString()}</span>,
    }),
    columnHelper.accessor('disponible', {
      header: 'Estado',
      cell: info => info.getValue() ? (
        <span className="inline-flex items-center gap-1 text-white bg-white/10 px-2 py-1 rounded-full text-[10px] font-black uppercase border border-white/10">
          <CheckCircle className="w-3 h-3 text-white" /> Disponible
        </span>
      ) : (
        <span className="inline-flex items-center gap-1 text-red-300 bg-red-500/20 px-2 py-1 rounded-full text-[10px] font-black uppercase border border-red-500/30">
          <XCircle className="w-3 h-3" /> Pausado
        </span>
      ),
    }),
    columnHelper.display({
      id: 'actions',
      header: 'Acciones',
      cell: info => (
        <div className="flex gap-2 justify-end">
          <Button 
            variant="secondary" 
            onClick={() => navigate(`/products/${info.row.original.id}`)} 
            className="!p-2 bg-white/10 text-white hover:bg-white/20 border border-white/10"
            title="Ver Detalle"
          >
            <Eye className="w-4 h-4" />
          </Button>
          <Button 
            variant="secondary" 
            onClick={() => onEdit(info.row.original)} 
            className="!p-2 bg-white/10 text-white hover:bg-white/20 border border-white/10"
            title="Editar"
          >
            <Pencil className="w-4 h-4" />
          </Button>
          <Button 
            variant="danger" 
            onClick={() => onDelete(info.row.original.id!)}
            className="!p-2 border border-red-500/30"
            title="Eliminar"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      ),
    }),
  ];

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="overflow-x-auto card !p-0 shadow-2xl">
      <table className="w-full text-left">
        <thead className="bg-cocoa border-b-2 border-cocoa/20">
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th key={header.id} className="px-6 py-4 text-xs font-black text-white uppercase tracking-wider">
                  {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="divide-y-2 divide-cocoa/20">
          {table.getRowModel().rows.map(row => (
            <tr key={row.id} className="hover:bg-cocoa/10 transition-colors">
              {row.getVisibleCells().map(cell => (
                <td key={cell.id} className="px-6 py-4">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
