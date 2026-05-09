import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppRouter } from './router/AppRouter';

// Motor de TanStack Query para toda la app
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    // QueryClientProvider envuelve todo para que cualquier componente pueda usar useQuery.
    // BrowserRouter vive dentro de AppRouter (patrón del profesor).
    <QueryClientProvider client={queryClient}>
      <AppRouter />
    </QueryClientProvider>
  );
}

export default App;
