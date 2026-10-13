import { useState } from 'react';

// Definicion de la estructura de datos esperada desde el endpoint FastAPI
interface GenerarResponse {
  resumen: string;
}

function App() {
  const [texto, setTexto] = useState<string>('');
  const [resumen, setResumen] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Purga de estados previos antes de iniciar una nueva transaccion
    setError('');
    setResumen('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/generar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ texto }),
      });

      // Evaluacion de codigos de estado HTTP fuera del rango 2xx
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Fallo de red o error interno en el servidor.');
      }

      const data: GenerarResponse = await response.json();
      setResumen(data.resumen);
    } catch (err: any) {
      setError(err.message);
    } finally {
      // Garantiza la liberacion de la interfaz independientemente del resultado de la peticion
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl w-full space-y-8 bg-white p-8 rounded-xl shadow-md border border-gray-100">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 text-center">
            Resumidor de Textos IA
          </h1>
          <p className="mt-2 text-sm text-gray-600 text-center">
            Introduce un texto y obtén un resumen conciso procesado por el backend.
          </p>
        </div>

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

        {/* Renderizado condicional de componentes de feedback */}
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
      </div>
    </div>
  );
}

export default App;
