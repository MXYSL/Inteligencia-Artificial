/*
* Programa para encontrar la ruta más corta en un grafo/laberinto usando Búsqueda en Anchura (BFS) y visualizarla en el DOM.
* Autor:
* Sánchez Gómez Alan Ivan
*/

import { sweetAlertSuccess, sweetAlertError } from "./util";

/**
 * Ejecuta el algoritmo de Búsqueda en Anchura (BFS) para encontrar el camino desde un nodo inicial hasta un nodo final.
 * A la par, interactúa con el DOM para animar la exploración coloreando los nodos evaluados.
 * @param graph - Un objeto/diccionario que representa el grafo mediante listas de adyacencia.
 * @param start - El ID del nodo donde comienza la búsqueda.
 * @param end - El ID del nodo objetivo que se desea alcanzar.
 * @param duration - El tiempo en milisegundos (retraso) entre la evaluación de cada nodo para la animación visual.
 * @returns Una promesa que resuelve con un arreglo de strings que representa la ruta desde el inicio hasta el fin, o null si no se encuentra ninguna ruta.
 */

export const bfs = async (graph: Record<string, string[]>, start: string, end: string, duration: number): Promise<string[] | null> => {
    const visited = new Set<string>();          // Arreglo de visitados
    const queue: string[] = [start];            // Cola
    const parents = new Map<string, string>();  //Mapa de padres (para reconstruir camino después)
    const delay = duration;                     // Duración para imprimir
    
    // Inicialización de métricas
    const startTime = performance.now();
    const startMemory = (performance as any).memory?.usedJSHeapSize || 0;
    let time_elapsed = 0;
    let memory_used = 0;

    // Colorea el nodo inicial para indicar el inicio de la búsqueda
    const initialNode = document.getElementById(start);
    if (initialNode) {
        initialNode.style.backgroundColor = 'rgb(76, 175, 80)';
    }

    visited.add(start); //Se agrega el nodo a visitados

    while (queue.length > 0) {
        const node = queue.shift()!; // Se obtiene el nodo actual de la cola
        
        // Colorea el nodo actual para indicar que está siendo evaluado
        const currentNode = document.getElementById(node);
        if (currentNode && currentNode.style.backgroundColor !== 'rgb(76, 175, 80)') {
            currentNode.style.backgroundColor = '#ffc107';
        }

        // Timer para animación, omite al primero
        if (node !== start) {
            await new Promise(resolve => setTimeout(resolve, delay)); // Timer para animación
        }

        // En caso de que llegamos la final
        if (node === end) {
            const path: string[] = [];
            let curr: string | undefined = end;
            
            // Reconstrucción de la ruta desde el nodo final hasta el nodo inicial utilizando el mapa de padres
            while (curr) {
                path.unshift(curr); // Se agrega al inicio del path
                const pathNode = document.getElementById(curr);
                if (pathNode) {
                    pathNode.style.backgroundColor = '#4caf50';
                }
                curr = parents.get(curr);
            }

            // Cálculo final de métricas (Éxito)
            time_elapsed = performance.now() - startTime; // Tiempo transcurrido en milisegundos
            memory_used = ((performance as any).memory?.usedJSHeapSize || 0) - startMemory; // Memoria utilizada en bytes
            console.log(`[BFS] Tiempo transcurrido: ${time_elapsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ms | Memoria añadida al Heap: ${memory_used.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} bytes`);
            sweetAlertSuccess(
            `Ruta encontrada en <b>${time_elapsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ms</b>.<br><br>Memoria añadida al Heap:<br><b>${memory_used.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} bytes</b>`
            );
            return path;
        }

        // Si no es el objetivo, agrega a los vecinos a la cola
        let contador = 0; // Contador para métricas (opcional)
        for (const neighbor of graph[node] || []) {
            if (!visited.has(neighbor)) {
                contador++; // Incrementa el contador por cada vecino evaluado
                visited.add(neighbor);
                parents.set(neighbor, node);
                queue.push(neighbor);
            }
        }

        if (currentNode && node !== start && node !== end && contador === 0) {
            currentNode.style.backgroundColor = '#ef5350';
        }
    }

    // Cálculo final de métricas (Sin ruta encontrada)
    time_elapsed = performance.now() - startTime;
    memory_used = ((performance as any).memory?.usedJSHeapSize || 0) - startMemory;
    console.log(`[BFS] Tiempo transcurrido: ${time_elapsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ms | Memoria añadida al Heap: ${memory_used.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} bytes (Ruta no encontrada)`);
    sweetAlertError(`No se encontró una ruta después de ${time_elapsed.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ms`);
    return null;
};