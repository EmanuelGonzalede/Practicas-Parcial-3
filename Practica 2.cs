// Creado por: Emanuel Gonzalez Ledesma

using System;
using System.Linq;

class SortingAlgorithms
{
    // Insertion Sort
    static void InsertionSort(int[] arr)
    {
        int n = arr.Length;
        for (int i = 1; i < n; i++)
        {
            int key = arr[i];
            int j = i - 1;
            while (j >= 0 && arr[j] > key)
            {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }

    // Selection Sort
    static void SelectionSort(int[] arr)
    {
        int n = arr.Length;
        for (int i = 0; i < n - 1; i++)
        {
            int minIdx = i;
            for (int j = i + 1; j < n; j++)
                if (arr[j] < arr[minIdx])
                    minIdx = j;
            int temp = arr[minIdx];
            arr[minIdx] = arr[i];
            arr[i] = temp;
        }
    }

    // Intercambio (Bubble Sort)
    static void BubbleSort(int[] arr)
    {
        int n = arr.Length;
        for (int i = 0; i < n - 1; i++)
            for (int j = 0; j < n - i - 1; j++)
                if (arr[j] > arr[j + 1])
                {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
    }

    // Ordenamiento de árbol (Heap Sort)
    static void HeapSort(int[] arr)
    {
        int n = arr.Length;
        for (int i = n / 2 - 1; i >= 0; i--)
            Heapify(arr, n, i);
        for (int i = n - 1; i > 0; i--)
        {
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            Heapify(arr, i, 0);
        }
    }

    static void Heapify(int[] arr, int n, int i)
    {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;

        if (left < n && arr[left] > arr[largest])
            largest = left;
        if (right < n && arr[right] > arr[largest])
            largest = right;
        if (largest != i)
        {
            int swap = arr[i];
            arr[i] = arr[largest];
            arr[largest] = swap;
            Heapify(arr, n, largest);
        }
    }

    // Quick Sort
    static void QuickSort(int[] arr, int low, int high)
    {
        if (low < high)
        {
            int pi = Partition(arr, low, high);
            QuickSort(arr, low, pi - 1);
            QuickSort(arr, pi + 1, high);
        }
    }

    static int Partition(int[] arr, int low, int high)
    {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; j++)
        {
            if (arr[j] < pivot)
            {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        int temp1 = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp1;
        return i + 1;
    }

    // Merge Sort
    static void MergeSort(int[] arr)
    {
        if (arr.Length <= 1)
            return;

        int mid = arr.Length / 2;
        int[] left = new int[mid];
        int[] right = new int[arr.Length - mid];

        Array.Copy(arr, 0, left, 0, mid);
        Array.Copy(arr, mid, right, 0, arr.Length - mid);

        MergeSort(left);
        MergeSort(right);

        Merge(arr, left, right);
    }

    static void Merge(int[] arr, int[] left, int[] right)
    {
        int i = 0, j = 0, k = 0;
        while (i < left.Length && j < right.Length)
        {
            if (left[i] <= right[j])
                arr[k++] = left[i++];
            else
                arr[k++] = right[j++];
        }
        while (i < left.Length)
            arr[k++] = left[i++];
        while (j < right.Length)
            arr[k++] = right[j++];
    }

    // Radix Sort
    static void RadixSort(int[] arr)
    {
        int max = arr.Max();
        for (int exp = 1; max / exp > 0; exp *= 10)
            CountSort(arr, exp);
    }

    static void CountSort(int[] arr, int exp)
    {
        int n = arr.Length;
        int[] output = new int[n];
        int[] count = new int[10];

        for (int i = 0; i < n; i++)
            count[(arr[i] / exp) % 10]++;

        for (int i = 1; i < 10; i++)
            count[i] += count[i - 1];

        for (int i = n - 1; i >= 0; i--)
        {
            output[count[(arr[i] / exp) % 10] - 1] = arr[i];
            count[(arr[i] / exp) % 10]--;
        }

        for (int i = 0; i < n; i++)
            arr[i] = output[i];
    }

    static void Main()
    {
        Console.WriteLine("Ingrese los elementos del array separados por comas:");
        int[] arr = Array.ConvertAll(Console.ReadLine().Split(','), int.Parse);

        Console.WriteLine("Seleccione el método de ordenamiento:");
        Console.WriteLine("1. Inserción (InsertionSort)");
        Console.WriteLine("2. Selección (SelectionSort)");
        Console.WriteLine("3. Intercambio (Bubble Sort)");
        Console.WriteLine("4. Ordenamiento de árbol (Heap Sort)");
        Console.WriteLine("5. QuickSort");
        Console.WriteLine("6. MergeSort");
        Console.WriteLine("7. RadixSort");

        int choice = int.Parse(Console.ReadLine());

        switch (choice)
        {
            case 1:
                InsertionSort(arr);
                break;
            case 2:
                SelectionSort(arr);
                break;
            case 3:
                BubbleSort(arr);
                break;
            case 4:
                HeapSort(arr);
                break;
            case 5:
                QuickSort(arr, 0, arr.Length - 1);
                break;
            case 6:
                MergeSort(arr);
                break;
            case 7:
                RadixSort(arr);
                break;
            default:
                Console.WriteLine("Opción no válida.");
                return;
        }

        Console.WriteLine("Array ordenado: " + string.Join(", ", arr));
    }
}
