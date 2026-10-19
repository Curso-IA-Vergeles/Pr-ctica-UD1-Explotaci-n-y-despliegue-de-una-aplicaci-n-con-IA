import { useState } from 'react';
import { SignedIn, SignedOut, SignInButton, UserButton, useAuth } from '@clerk/clerk-react';

// Contrato de interfaz para la respuesta JSON del servidor
interface GenerarResponse {
  resumen: string;
}

function App() {
  const [texto, setTexto] = useState<string>('');
  const [resumen, setResumen] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  // Hook de sesion para extraer el JWT activo del usuario autenticado
  const { getToken } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Limpieza de estados de feedback antes de emitir una nueva consulta
    setError('');
    setResumen('');
    setIsLoading(true);

    try {
      const token = await getToken();

      const response = await fetch('/api/generar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify({ texto }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || `Error HTTP ${response.status} al procesar la solicitud.`);
      }

      const data: GenerarResponse = await response.json();
      setResumen(data.resumen);
    } catch (err: any) {
      setError(err.message);
    } finally {
      // Restablecimiento del bloqueo de interfaz tras finalizar la promesa
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
      {/* Cabecera de control de sesion activa */}
      <header className="w-full max-w-2xl flex justify-end mb-4">
        <SignedIn>
          <UserButton />
        </SignedIn>
      </header>

      <div className="max-w-2xl w-full space-y-8 bg-white p-8 rounded-xl shadow-md border border-gray-100">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 text-center">
            Resumidor de Textos IA
          </h1>
          <p className="mt-2 text-sm text-gray-600 text-center">
            Introduce un texto y obtén un resumen conciso procesado por el backend.
          </p>
        </div>

        {/* Vista publica para usuarios no autenticados */}
        <SignedOut>
          <div className="flex flex-col items-center justify-center mt-8 space-y-4">
            <p className="text-sm text-gray-500">Inicia sesión con tu cuenta para utilizar la herramienta.</p>
            <SignInButton mode="modal">
              <button className="py-2 px-6 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 transition-colors">
                Iniciar Sesión
              </button>
            </SignInButton>
          </div>
        </SignedOut>

        {/* Vista protegida accesible unicamente con sesion iniciada */}
        <SignedIn>
          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            <div>
              <label htmlFor="texto" className="block text-sm font-medium text-gray-700">
                Payload de entrada
              </label>
              <div className="mt-1">
                <textarea
                  id="texto"
                  name="texto"
                  rows={6}
                  className="shadow-sm focus:ring-blue-500 focus:border-blue-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md p-3"
                  placeholder="Inserta el texto a procesar..."
                  value={texto}
                  onChange={(e) => setTexto(e.target.value)}
                  required
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={isLoading || !texto.trim()}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Procesando request...' : 'Generar Resumen'}
              </button>
            </div>
          </form>

          {error && (
            <div className="rounded-md bg-red-50 p-4 mt-4 border border-red-200">
              <h3 className="text-sm font-medium text-red-800">Excepción capturada</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          )}

          {resumen && (
            <div className="rounded-md bg-green-50 p-4 mt-4 border border-green-200">
              <h3 className="text-sm font-medium text-green-800">Salida del modelo</h3>
              <div className="mt-2 text-sm text-green-700">
                <p>{resumen}</p>
              </div>
            </div>
          )}
        </SignedIn>
      </div>
    </div>
  );
}

export default App;