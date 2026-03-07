/*
* Programa para encontrar una ruta en un grafo/laberinto usando Búsqueda en Profundidad (DFS) y visualizarla en el DOM.
* Autor:
* Sánchez Gómez Alan Ivan
*/

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
        return path;
    }
    return null;
};