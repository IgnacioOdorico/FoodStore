import React, { useMemo } from 'react';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import type { Categoria } from '../types/categoria';
import { Button } from '../../../shared/ui/Button';
import { Pencil, Trash2, Image as ImageIcon } from 'lucide-react';

interface CategoriaTableProps {
  data: Categoria[];
  onEdit: (categoria: Categoria) => void;
  onDelete: (id: number) => void;
}

const columnHelper = createColumnHelper<Categoria & { depth: number }>();

export const CategoriaTable: React.FC<CategoriaTableProps> = ({ data, onEdit, onDelete }) => {
  // Función para aplanar la jerarquía y calcular la profundidad con protección contra ciclos
  const flattenedData = useMemo(() => {
    const visited = new Set<number>();
    
    const flatten = (
      cats: Categoria[], 
      parentId: number | null = null, 
      depth = 0
    ): (Categoria & { depth: number })[] => {
      if (depth > 10) return []; // Seguridad total contra recursión infinita
      return cats
        .filter(c => c.parent_id === parentId)
        .reduce((acc, cat) => {
          if (visited.has(cat.id!)) return acc;
          visited.add(cat.id!);

          return [
            ...acc, 
            { ...cat, depth }, 
            ...flatten(cats, cat.id!, depth + 1)
          ];
        }, [] as (Categoria & { depth: number })[]);
    };

    return flatten(data);
  }, [data]);

  const columns = [
    columnHelper.accessor('imagen_url', {
      header: 'Imagen',
      cell: info => {
        const url = info.getValue();
        return (
          <div className="w-10 h-10 rounded-lg overflow-hidden bg-gray-100 flex-shrink-0 border border-gray-100">
            {url ? (
              <img src={url} alt="Categoría" className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                <ImageIcon className="w-5 h-5" />
              </div>
            )}
          </div>
        );
      },
    }),
    columnHelper.accessor('nombre', {
      header: 'Nombre',
      cell: info => {
        const depth = info.row.original.depth;
        return (
          <div className="flex items-center gap-2" style={{ paddingLeft: `${depth * 24}px` }}>
            {depth > 0 && <span className="text-gray-300">└─</span>}
            <span className="font-semibold text-gray-900">{info.getValue()}</span>
          </div>
        );
      },
    }),
    columnHelper.accessor('descripcion', {
      header: 'Descripción',
      cell: info => <span className="text-gray-600 line-clamp-1">{info.getValue() || '-'}</span>,
    }),
    columnHelper.display({
      id: 'actions',
      header: 'Acciones',
      cell: info => (
        <div className="flex gap-2 justify-end">
          <Button 
            variant="secondary" 
            onClick={() => onEdit(info.row.original)}
            className="!p-2"
          >
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
    data: flattenedData,
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
                  {header.isPlaceholder
                    ? null
                    : flexRender(header.column.columnDef.header, header.getContext())}
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
