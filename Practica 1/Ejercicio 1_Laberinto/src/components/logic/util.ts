//Component to save utility functions for the logic of the game

import { MazeCell } from "../interfaces/maze";

// Function to get a random integer between min and max (inclusive)
export const getRandomInt = (min: number, max: number): number => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

// Function to transform a maze represented as a 2D array of MazeCell into an adjacency list for graph representation
export const mazeToGraph = (maze: MazeCell[][]): Record<string, string[]> => {
  const graph: Record<string, string[]> = {};
  
  for (let row of maze) {
    for (let cell of row) {
      const key = `${cell.x}-${cell.y}`;
      graph[key] = [];
      
      if (!cell.top) graph[key].push(`${cell.x}-${cell.y - 1}`); // Connect to the cell above
      if (!cell.right) graph[key].push(`${cell.x + 1}-${cell.y}`); // Connect to the cell on the right
      if (!cell.bottom) graph[key].push(`${cell.x}-${cell.y + 1}`); // Connect to the cell below
      if (!cell.left) graph[key].push(`${cell.x - 1}-${cell.y}`); // Connect to the cell on the left
    }
  }
  
  return graph;
}

export const cleanUpColors = (maze: MazeCell[][]) => {
  for (let row of maze) {
    for (let cell of row) {
      const node = document.getElementById(`${cell.x}-${cell.y}`);
      if (node) {
        node.style.backgroundColor = '#f8f9fa'; // Reset to default color
      }
    }
  }
};
