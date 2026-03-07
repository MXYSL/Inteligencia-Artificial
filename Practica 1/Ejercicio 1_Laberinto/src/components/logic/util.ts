/*
* Módulo de funciones de utilidad para la lógica del laberinto
* Funciones:
* - getRandomInt: Genera un número entero aleatorio dentro de un rango específico.
* - mazeToGraph: Transforma la matriz del laberinto en un grafo usando listas de adyacencia.
* - cleanUpColors: Restablece el color de fondo por defecto de las celdas en el DOM.
* - sweetAlertSuccess: Muestra una alerta modal de éxito usando SweetAlert2.
* - sweetAlertError: Muestra una alerta modal de error usando SweetAlert2.
* Autor:
* Sánchez Gómez Alan Ivan
*/

import { MazeCell } from "../interfaces/maze";
import Swal from 'sweetalert2';

/**
 * Obtiene un número entero aleatorio entre un valor mínimo y máximo (ambos inclusivos).
 */
export const getRandomInt = (min: number, max: number): number => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

/**
 * Convierte un laberinto representado en un arreglo bidimensional (matriz) a una estructura de grafo (lista de adyacencia).
 */
export const mazeToGraph = (maze: MazeCell[][]): Record<string, string[]> => {
  const graph: Record<string, string[]> = {};
  
  for (let row of maze) {
    for (let cell of row) {
      const key = `${cell.x}-${cell.y}`;
      graph[key] = [];
      
      if (!cell.top) graph[key].push(`${cell.x}-${cell.y - 1}`);
      if (!cell.right) graph[key].push(`${cell.x + 1}-${cell.y}`);
      if (!cell.bottom) graph[key].push(`${cell.x}-${cell.y + 1}`);
      if (!cell.left) graph[key].push(`${cell.x - 1}-${cell.y}`);
    }
  }
  
  return graph;
}

/**
 * Recorre todas las celdas del laberinto y restablece su color original en el DOM.
 */
export const cleanUpColors = (maze: MazeCell[][]) => {
  for (let row of maze) {
    for (let cell of row) {
      const node = document.getElementById(`${cell.x}-${cell.y}`);
      if (node) {
        node.style.backgroundColor = '#f8f9fa';
      }
    }
  }
};

/**
 * Muestra un mensaje emergente de éxito (Toast).
 */
export const sweetAlertSuccess = (message: string) => {
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'success',
    title: '¡Éxito! Detalles en la consola',
    html: message, // <--- Cambiado de 'text' a 'html'
    showConfirmButton: false,
    timer: 10000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer);
      toast.addEventListener('mouseleave', Swal.resumeTimer);
    }
  });
};

/**
 * Muestra un mensaje emergente de error (Toast).
 */
export const sweetAlertError = (message: string) => {
  Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'error',
    title: '¡Error! Detalles en la consola',
    html: message, // <--- Cambiado de 'text' a 'html'
    showConfirmButton: false,
    timer: 10000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer);
      toast.addEventListener('mouseleave', Swal.resumeTimer);
    }
  });
}