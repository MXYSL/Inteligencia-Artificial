/*
* Programa para encontrar una ruta en un grafo/laberinto usando Búsqueda en Profundidad (DFS) y visualizarla en el DOM.
* Autor:
* Sánchez Gómez Alan Ivan
*/

import { sweetAlertSuccess, sweetAlertError } from "./util";

/**
 * Ejecuta el algoritmo de Búsqueda en Profundidad (DFS) para encontrar un camino desde un nodo inicial hasta un nodo final.
 * Explora cada rama lo más profundo posible antes de retroceder (backtracking), animando los pasos en el DOM.
 * @param graph - Un objeto/diccionario que representa el grafo mediante listas de adyacencia.
 * @param start - El ID del nodo donde comienza la búsqueda.
 * @param end - El ID del nodo objetivo que se desea alcanzar.
 * @param duration - El tiempo en milisegundos (retraso) entre la evaluación de cada nodo para la animación visual.
 * @returns Una promesa que resuelve con un arreglo de strings que representa la ruta desde el inicio hasta el fin, o null si no se encuentra ninguna ruta.
 */
export const dfs = async (graph: Record<string, string[]>, start: string, end: string, duration: number): Promise<string[] | null> => {
    const visited = new Set<string>();
    const path: string[] = [];
    const delay = duration;
    const initialNode = document.getElementById(start);

    // Inicialización de métricas
    const startTime = performance.now();
    const startMemory = (performance as any).memory?.usedJSHeapSize || 0;
    let time_elapsed = 0;
    let memory_used = 0;

    if (initialNode) {
        initialNode.style.backgroundColor = 'rgb(76, 175, 80)';
    }

    const dfsHelper = async (node: string): Promise<boolean> => {
        const currentNode = document.getElementById(node);
        if (currentNode && currentNode.style.backgroundColor !== 'rgb(76, 175, 80)') {
            currentNode.style.backgroundColor = '#ffc107';
        }
        
        if (visited.has(node)) return false;
        visited.add(node);
        path.push(node);

        await new Promise(resolve => setTimeout(resolve, delay));

        if (node === end) {
            if (currentNode) {
                currentNode.style.backgroundColor = '#4caf50';
            }
            return true;
        }

        for (const neighbor of graph[node] || []) {
            if (await dfsHelper(neighbor)) return true;
        }

        path.pop();
        if (currentNode) {
            currentNode.style.backgroundColor = '#ef5350';
        }
        
        await new Promise(resolve => setTimeout(resolve, delay));
        return false;
    };

    if (await dfsHelper(start)) {
        for (const node of path) {
            const pathNode = document.getElementById(node);
            if (pathNode) {
                pathNode.style.backgroundColor = '#4caf50';
            }
        }
        // Cálculo final de métricas (Éxito)
            time_elapsed = performance.now() - startTime;
            memory_used = ((performance as any).memory?.usedJSHeapSize || 0) - startMemory;
            console.log(`[DFS] Tiempo transcurrido: ${time_elapsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ms | Memoria añadida al Heap: ${memory_used.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} bytes (Ruta encontrada)`);
            sweetAlertSuccess(
            `Ruta encontrada en <b>${time_elapsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ms</b>.<br><br>Memoria añadida al Heap:<br><b>${memory_used.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} bytes</b>`
            );        
            return path;
    }
    // Cálculo final de métricas (Sin ruta encontrada)
    time_elapsed = performance.now() - startTime;
    memory_used = ((performance as any).memory?.usedJSHeapSize || 0) - startMemory;
    console.log(`[DFS] Tiempo transcurrido: ${time_elapsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ms | Memoria añadida al Heap: ${memory_used.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} bytes (Ruta no encontrada)`);
    sweetAlertError(`No se encontró una ruta después de ${time_elapsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ms`);
    return null;
};