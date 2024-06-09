//Creado por: Emanuel Gonzalez Ledesma-21110398

using System;
using System.Collections.Generic;

class DijkstraSimulator
{
    static void Main(string[] args)
    {
        // Creamos un grafo de ejemplo
        int[,] graph = {
            { 0, 4, 0, 0, 0, 0, 0, 8, 0 },
            { 4, 0, 8, 0, 0, 0, 0, 11, 0 },
            { 0, 8, 0, 7, 0, 4, 0, 0, 2 },
            { 0, 0, 7, 0, 9, 14, 0, 0, 0 },
            { 0, 0, 0, 9, 0, 10, 0, 0, 0 },
            { 0, 0, 4, 0, 10, 0, 2, 0, 0 },
            { 0, 0, 0, 14, 0, 2, 0, 1, 6 },
            { 8, 11, 0, 0, 0, 0, 1, 0, 7 },
            { 0, 0, 2, 0, 0, 0, 6, 7, 0 }
        };

        Dijkstra(graph, 0);
    }

    static void Dijkstra(int[,] graph, int source)
    {
        int numVertices = graph.GetLength(0);
        int[] dist = new int[numVertices];
        bool[] visited = new bool[numVertices];

        for (int i = 0; i < numVertices; i++)
        {
            dist[i] = int.MaxValue;
            visited[i] = false;
        }

        dist[source] = 0;

        for (int count = 0; count < numVertices - 1; count++)
        {
            int u = MinDistance(dist, visited);
            visited[u] = true;

            Console.WriteLine($"Paso {count + 1}:");
            Console.WriteLine($"Nodo {u} visitado.");

            for (int v = 0; v < numVertices; v++)
            {
                if (!visited[v] && graph[u, v] != 0 && dist[u] != int.MaxValue && dist[u] + graph[u, v] < dist[v])
                {
                    dist[v] = dist[u] + graph[u, v];
                    Console.WriteLine($"Distancia mínima a nodo {v} actualizada a {dist[v]}.");
                }
            }
            Console.WriteLine();
        }

        Console.WriteLine("Distancias mínimas desde el nodo origen:");
        for (int i = 0; i < numVertices; i++)
        {
            Console.WriteLine($"Nodo {i}: {dist[i]}");
        }
    }

    static int MinDistance(int[] dist, bool[] visited)
    {
        int min = int.MaxValue;
        int minIndex = -1;

        for (int v = 0; v < dist.Length; v++)
        {
            if (!visited[v] && dist[v] <= min)
            {
                min = dist[v];
                minIndex = v;
            }
        }

        return minIndex;
    }
}
