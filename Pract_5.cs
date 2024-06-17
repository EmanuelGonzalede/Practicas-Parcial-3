using System;
using System.Collections.Generic;

class Edge : IComparable<Edge>
{
    public int Source { get; }
    public int Destination { get; }
    public int Weight { get; }

    public Edge(int source, int destination, int weight)
    {
        Source = source;
        Destination = destination;
        Weight = weight;
    }

    public int CompareTo(Edge other)
    {
        return Weight.CompareTo(other.Weight);
    }

    public override string ToString()
    {
        return $"{Source} -- {Destination} == {Weight}";
    }
}

class Graph
{
    private int vertices;
    private List<Edge> edges;

    public Graph(int vertices)
    {
        this.vertices = vertices;
        edges = new List<Edge>();
    }

    public void AddEdge(int source, int destination, int weight)
    {
        edges.Add(new Edge(source, destination, weight));
    }

    public void KruskalMST(bool findMin)
    {
        if (findMin)
        {
            edges.Sort();
        }
        else
        {
            edges.Sort((a, b) => b.Weight.CompareTo(a.Weight));
        }

        int[] parent = new int[vertices];
        for (int i = 0; i < vertices; i++)
        {
            parent[i] = i;
        }

        List<Edge> mst = new List<Edge>();
        int index = 0;

        while (mst.Count < vertices - 1 && index < edges.Count)
        {
            Edge edge = edges[index++];
            int sourceRoot = Find(parent, edge.Source);
            int destinationRoot = Find(parent, edge.Destination);

            if (sourceRoot != destinationRoot)
            {
                mst.Add(edge);
                Union(parent, sourceRoot, destinationRoot);
                Console.WriteLine($"Borde {edge} añadido al MST.");
            }
        }

        Console.WriteLine("\nMST resultante:");
        foreach (Edge edge in mst)
        {
            Console.WriteLine(edge);
        }
    }

    private int Find(int[] parent, int vertex)
    {
        if (parent[vertex] != vertex)
        {
            parent[vertex] = Find(parent, parent[vertex]);
        }
        return parent[vertex];
    }

    private void Union(int[] parent, int sourceRoot, int destinationRoot)
    {
        parent[sourceRoot] = destinationRoot;
    }
}

class Program
{
    static void Main(string[] args)
    {
        Graph graph = new Graph(6);
        graph.AddEdge(0, 1, 4);
        graph.AddEdge(0, 2, 4);
        graph.AddEdge(1, 2, 2);
        graph.AddEdge(1, 3, 6);
        graph.AddEdge(2, 3, 8);
        graph.AddEdge(3, 4, 9);
        graph.AddEdge(4, 5, 10);
        graph.AddEdge(3, 5, 1);

        Console.WriteLine("MST (Costo Mínimo) de Kruskal):");
        graph.KruskalMST(true);

        Console.WriteLine("\nMST (Coste Máximo) de Kruskal:");
        graph.KruskalMST(false);
    }
}
