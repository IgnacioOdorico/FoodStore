import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Navbar } from './components/Navbar';
import { CategoriesPage } from './pages/CategoriesPage';
import { ProductsPage } from './pages/ProductsPage';
import { IngredientsPage } from './pages/IngredientsPage';
import { ProductDetailPage } from './pages/ProductDetailPage';

// CREO EL QUERY CLIENT: Este es el motor de TanStack Query para toda la app.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Puse esto en false para que no me vuelva a pedir los datos cada vez que cambio de ventana.
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    // QueryClientProvider: Envuelvo todo para que cualquier componente pueda usar useQuery.
    <QueryClientProvider client={queryClient}>
      {/* BrowserRouter: Maneja la navegación sin recargar la página (SPA) */}
      <BrowserRouter>
        <div className="min-h-screen bg-canvas">
          <Navbar />

          {/* pt-40: Padding ideal para el Navbar restaurado (h-32) */}
          <main className="container mx-auto px-4 pt-40 pb-12">
            <Routes>
              {/* Si entran a la raíz, los mando directo a Productos */}
              <Route path="/" element={<Navigate to="/products" replace />} />

              {/* RUTAS PRINCIPALES */}
              <Route path="/categories" element={<CategoriesPage />} />
              <Route path="/products" element={<ProductsPage />} />

              {/* RUTA DINÁMICA: El ':id' es un parámetro que después capturo con 'useParams' en el detalle. */}
              <Route path="/products/:id" element={<ProductDetailPage />} />

              <Route path="/ingredients" element={<IngredientsPage />} />

              {/* Si ponen cualquier otra cosa en la URL, los mando a Categorías */}
              <Route path="*" element={<Navigate to="/categories" replace />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
