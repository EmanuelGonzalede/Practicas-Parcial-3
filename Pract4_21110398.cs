using System;
using System.Collections.Generic;

class PrimSimulator
{
    static void Main(string[] args)
    {
        // Creamos un grafo de ejemplo como una lista de adyacencia
        Dictionary<int, List<(int, int)>> graph = new Dictionary<int, List<(int, int)>>
        {
            { 0, new List<(int, int)> { (1, 4), (7, 8) } },
            { 1, new List<(int, int)> { (0, 4), (7, 11), (2, 8) } },
            { 2, new List<(int, int)> { (1, 8), (8, 2), (5, 4), (3, 7) } },
            { 3, new List<(int, int)> { (2, 7), (5, 14), (4, 9) } },
            { 4, new List<(int, int)> { (3, 9), (5, 10) } },
            { 5, new List<(int, int)> { (4, 10), (3, 14), (2, 4), (6, 2) } },
            { 6, new List<(int, int)> { (5, 2), (7, 1), (8, 6) } },
            { 7, new List<(int, int)> { (0, 8), (1, 11), (6, 1), (8, 7) } },
            { 8, new List<(int, int)> { (2, 2), (6, 6), (7, 7) } }
        };

        PrimMST(graph);
    }

    static void PrimMST(Dictionary<int, List<(int, int)>> graph)
    {
        int numVertices = graph.Count;
        int[] parent = new int[numVertices];
        int[] key = new int[numVertices];
        bool[] mstSet = new bool[numVertices];

        for (int i = 0; i < numVertices; i++)
        {
            key[i] = int.MaxValue;
            mstSet[i] = false;
        }

        key[0] = 0; // Seleccionamos el primer vértice como raíz del árbol mínimo
        parent[0] = -1; // No tiene padre

        for (int count = 0; count < numVertices - 1; count++)
        {
            int u = MinKey(key, mstSet);
            mstSet[u] = true;

            Console.WriteLine($"Paso {count + 1}:");
            Console.WriteLine($"Arista añadida: ({parent[u]}, {u}), Peso: {key[u]}");

            // Actualizamos las claves de los vértices adyacentes a u
            foreach (var vertex in graph[u])
            {
                int v = vertex.Item1;
                int weight = vertex.Item2;
                if (!mstSet[v] && weight < key[v])
                {
                    parent[v] = u;
                    key[v] = weight;
                }
            }
            Console.WriteLine();
        }
    }

    static int MinKey(int[] key, bool[] mstSet)
    {
        int min = int.MaxValue;
        int minIndex = -1;

        for (int v = 0; v < key.Length; v++)
        {
            if (!mstSet[v] && key[v] < min)
            {
                min = key[v];
                minIndex = v;
            }
        }

        return minIndex;
    }
}

