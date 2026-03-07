/*
* Programa para encontrar la ruta más corta en un grafo/laberinto usando Búsqueda en Anchura (BFS) y visualizarla en el DOM.
* Autor:
* Sánchez Gómez Alan Ivan
*/

/**
 * Ejecuta el algoritmo de Búsqueda en Anchura (BFS) para encontrar el camino desde un nodo inicial hasta un nodo final.
 * A la par, interactúa con el DOM para animar la exploración coloreando los nodos evaluados.
 * * @param graph - Un objeto/diccionario que representa el grafo mediante listas de adyacencia.
 * @param start - El ID del nodo donde comienza la búsqueda.
 * @param end - El ID del nodo objetivo que se desea alcanzar.
 * @param duration - El tiempo en milisegundos (retraso) entre la evaluación de cada nodo para la animación visual.
 * @returns Una promesa que resuelve con un arreglo de strings que representa la ruta desde el inicio hasta el fin, o null si no se encuentra ninguna ruta.
 */

export const bfs = async (graph: Record<string, string[]>, start: string, end: string, duration: number): Promise<string[] | null> => {
    const visited = new Set<string>();
    const queue: string[] = [start];
    const parents = new Map<string, string>();
    const delay = duration;

    // Colorea el nodo inicial para indicar el inicio de la búsqueda
    const initialNode = document.getElementById(start);
    if (initialNode) {
        initialNode.style.backgroundColor = 'rgb(76, 175, 80)';
    }

    visited.add(start);

    while (queue.length > 0) {
        const node = queue.shift()!;
        
        const currentNode = document.getElementById(node);
        if (currentNode && currentNode.style.backgroundColor !== 'rgb(76, 175, 80)') {
            currentNode.style.backgroundColor = '#ffc107';
        }

        if (node !== start) {
            await new Promise(resolve => setTimeout(resolve, delay));
        }

        if (node === end) {
            const path: string[] = [];
            let curr: string | undefined = end;
            
            while (curr) {
                path.unshift(curr);
                const pathNode = document.getElementById(curr);
                if (pathNode) {
                    pathNode.style.backgroundColor = '#4caf50';
                }
                curr = parents.get(curr);
            }
            return path;
        }

        for (const neighbor of graph[node] || []) {
            if (!visited.has(neighbor)) {
                visited.add(neighbor);
                parents.set(neighbor, node);
                queue.push(neighbor);
            }
        }

        if (currentNode && node !== start) {
            currentNode.style.backgroundColor = '#ef5350';
        }
    }

    return null;
};