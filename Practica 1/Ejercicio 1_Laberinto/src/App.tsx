/*
* Módulo principal de visualización y control del laberinto
* Funciones:
* - MazeBoard: Componente principal que maneja el estado y la interfaz de usuario.
* - handleGenerateMaze: Genera un nuevo laberinto basado en el tamaño ingresado por el usuario.
* - handleResetColors: Limpia los colores de exploración del laberinto actual.
* - terminate: Reinicia la aplicación recargando la página completa.
* - handleStart: Ejecuta el algoritmo seleccionado (DFS o BFS) sobre el laberinto generado.
* Autor:
* Sánchez Gómez Alan Ivan
*/

// Importación de hooks de React y dependencias externas
import { useState, useEffect } from 'react';
import generateMaze from 'generate-maze';
// Importación de interfaces, algoritmos y utilidades
import { MazeCell } from './components/interfaces/maze';
import { dfs } from "./components/logic/dfs";
import { bfs } from "./components/logic/bfs";
import { getRandomInt, mazeToGraph, cleanUpColors } from "./components/logic/util";
import './App.css';

export default function MazeBoard() {
  // Definición de los estados del componente para el laberinto, configuración y UI
  const [maze, setMaze] = useState<MazeCell[][]>([]);
  const [activeSize, setActiveSize] = useState<number>(1);
  const [inputSize, setInputSize] = useState<number>(1);
  const [duration, setDuration] = useState<number>(100);
  const [algorithm, setAlgorithm] = useState<string>('dfs');
  const [refreshKey, setRefreshKey] = useState<number>(0);

  // Hook que genera un laberinto nuevo cada vez que cambia el tamaño activo o la clave de refresco
  useEffect(() => {
    const newMaze = generateMaze(activeSize, activeSize, true, getRandomInt(0, 10000)) as MazeCell[][];
    setMaze(newMaze);
  }, [activeSize, refreshKey]);

  // Manejador para aplicar un nuevo tamaño y disparar la regeneración del laberinto
  const handleGenerateMaze = () => {
    handleResetColors(); 
    setActiveSize(inputSize);
    setRefreshKey(prev => prev + 1);
  };

  // Manejador para borrar los rastros de colores de la búsqueda anterior
  const handleResetColors = () => {
    cleanUpColors(maze);
  }

  // Manejador para refrescar la ventana y reiniciar por completo
  const terminate = () => {
    window.location.reload();
  }

  // Manejador principal para iniciar la resolución del laberinto con el algoritmo elegido
  const handleStart = async () => {
    const result = await (algorithm === 'dfs' ? dfs : bfs)(
      mazeToGraph(maze), 
      '0-0', 
      `${activeSize - 1}-${activeSize - 1}`, 
      duration
    );

    console.log(`${algorithm.toUpperCase()} Result:`, result);
  };

  return (
    // Contenedor principal del layout
    <div className="app-layout">

      {/* Contenedor del panel de controles */}
      <div className="controls-container">
        
        {/* Selector controlado para elegir entre el algoritmo DFS o BFS */}
        <select 
          className="styled-select"
          value={algorithm}
          onChange={(e) => setAlgorithm(e.target.value)}
        >
          <option value="dfs">DFS</option>
          <option value="bfs">BFS</option>
        </select>

        {/* Campo de entrada controlado para definir el tamaño de la cuadrícula */}
        <input
          type="text"
          className="styled-select"
          placeholder="Size"
          min="4"
          value={inputSize}
          onChange={(e) => setInputSize(Number(e.target.value))}
        />

        {/* Campo de entrada controlado para ajustar la velocidad (duración en ms) */}
        <input
          type="text"
          className="styled-select"
          placeholder="Duración (ms)"
          min="1"
          value={duration}
          onChange={(e) => setDuration(Number(e.target.value))}
        />

        {/* Botones de acción para interactuar con la aplicación */}
        <button className="btn-secondary" onClick={handleGenerateMaze}>
          Generate New Maze
        </button>
        <button className="btn-secondary" onClick={handleResetColors}>
          Reset colors
        </button>
        <button className="btn-secondary" onClick={terminate}>
          Reset
        </button>
        <button className="btn-primary" onClick={handleStart}>
          Start
        </button>
      </div>

      {/* Contenedor que envuelve y muestra la cuadrícula del laberinto */}
      <div className="maze-wrapper flex-grow">
        <h2 className="maze-title">Ejercicio de Laberinto</h2>

        {/* Renderizado dinámico de las filas y celdas generadas */}
        <div style={{ display: 'inline-flex', flexDirection: 'column' }}>
          {maze.map((row, rowIndex) => (
            <div key={rowIndex} style={{ display: 'flex' }}>
              {row.map((cell) => (
                // Renderizado de cada celda individual configurando sus bordes para simular las paredes
                <div
                  key={`${cell.x}-${cell.y}`}
                  id={`${cell.x}-${cell.y}`}
                  style={{
                    width: '40px',
                    height: '40px',
                    backgroundColor: '#f8f9fa',
                    boxSizing: 'border-box',
                    borderTop: cell.top ? '2px solid #333' : '2px solid transparent',
                    borderRight: cell.right ? '2px solid #333' : '2px solid transparent',
                    borderBottom: cell.bottom ? '2px solid #333' : '2px solid transparent',
                    borderLeft: cell.left ? '2px solid #333' : '2px solid transparent',
                  }}
                />
              ))}
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}