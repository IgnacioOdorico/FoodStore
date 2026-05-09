import React from 'react';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import type { Ingrediente } from '../types/ingrediente';
import { Button } from '../../../shared/ui/Button';
import { Pencil, Trash2, Package } from 'lucide-react';

interface IngredientTableProps {
  data: Ingrediente[];
  onEdit: (ingrediente: Ingrediente) => void;
  onDelete: (id: number) => void;
}

const columnHelper = createColumnHelper<Ingrediente>();

export const IngredientTable: React.FC<IngredientTableProps> = ({ data, onEdit, onDelete }) => {
  const columns = [
    columnHelper.accessor('nombre', {
      header: 'Ingrediente',
      cell: info => (
        <div className="flex items-center gap-3">
          <div className="bg-white/10 text-orange-400 p-2 rounded-lg">
            <Package className="w-5 h-5" />
          </div>
          <div className="flex flex-col">
            <span className="font-semibold text-white">{info.getValue()}</span>
            {info.row.original.es_alergeno && (
              <span className="text-[10px] bg-red-500/20 text-red-300 px-1.5 py-0.5 rounded font-bold uppercase w-fit mt-0.5 border border-red-500/30">
                Alérgeno
              </span>
            )}
          </div>
        </div>
      ),
    }),
    columnHelper.accessor('descripcion', {
      header: 'Descripción',
      cell: info => <span className="text-white/60 line-clamp-1">{info.getValue() || '-'}</span>,
    }),
    columnHelper.display({
      id: 'actions',
      header: 'Acciones',
      cell: info => (
        <div className="flex gap-2 justify-end">
          <Button variant="secondary" onClick={() => onEdit(info.row.original)} className="!p-2">
            <Pencil className="w-4 h-4" />
          </Button>
          <Button 
            variant="danger" 
            onClick={() => onDelete(info.row.original.id!)}
            className="!p-2"
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
    <div className="overflow-x-auto card !p-0">
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
