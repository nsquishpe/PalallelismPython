import os  # interactúa con el sistema operativo
import psutil  #  información sobre el sistema 
import multiprocessing  # maneja la ejecución de procesos en paralelo

# selection_sort
def selection_sort(numbers, start, end):
    for i in range(start, end):
        max_index = i
        for j in range(i + 1, end):
            if numbers[j] > numbers[max_index]:
                max_index = j
        numbers[i], numbers[max_index] = numbers[max_index], numbers[i]

# Encuentra el máximo y meide recursos
def find_max(numbers, start, end, result, process_num):
    steps = 0  # Contador de pasos
    selection_sort(numbers, start, end)  # Ordenar el fragmento de la lista
    max_num = numbers[start]  # Encontrar el máximo del fragmento
    steps += end - start  # Contar los pasos realizados
    # Medir el uso de CPU antes de poner los resultados en la cola
    cpu_percent = psutil.Process(os.getpid()).cpu_percent(interval=0.01)
    # Medir el uso de memoria antes de poner los resultados en la cola
    memory_percent = psutil.Process(os.getpid()).memory_percent()
    result.put((max_num, cpu_percent, memory_percent, steps))

if __name__ == "__main__":
    # Obtener información del sistema
    cpu_count = multiprocessing.cpu_count()  # Número de núcleos de CPU
    ram_percent = psutil.virtual_memory().percent  # Porcentaje de uso de RAM

    # Definir la lista de números
    numbers = [85, 23, 47, 12, 63, 91, 75, 36, 18, 7, 52, 44, 99, 26, 61, 68, 57, 41, 88, 33, 79, 95, 29, 59, 22, 3, 72, 15, 70, 49, 92, 66, 5, 81, 39, 14, 30, 97, 9, 64, 53, 76, 60, 84, 2, 43, 20, 78, 25, 11, 46, 31, 67, 93, 17, 28, 74, 89, 50, 55, 69, 96, 65, 21, 58, 82, 87, 38, 16, 35, 1, 73, 54, 83, 40, 27, 94, 10, 8, 80, 48, 19, 45, 32, 13, 86, 90, 37, 71, 4, 56, 62, 24, 98, 51, 6, 34, 100]

    # Calcular el tamaño de cada fragmento de la lista
    chunk_size = len(numbers) // cpu_count
    # Crear una cola para almacenar los resultados de los procesos
    result_queue = multiprocessing.Queue()
    # Crear una lista para almacenar los objetos de proceso
    processes = []

    # Crear y lanzar procesos para ejecutar find_max en paralelo
    for i in range(cpu_count):
        start = i * chunk_size
        end = start + chunk_size if i < cpu_count - 1 else len(numbers)
        # Crear un proceso con la función find_max y los argumentos necesarios
        process = multiprocessing.Process(target=find_max, args=(numbers, start, end, result_queue, i))
        processes.append(process)  # Agregar el proceso a la lista
        process.start()  # Iniciar el proceso

    # Esperar a que todos los procesos terminen
    for process in processes:
        process.join()

    # Inicializar listas para almacenar los resultados
    max_numbers = []
    cpu_percentages = []
    memory_percentages = []  # Lista para almacenar los porcentajes de memoria
    steps_per_core = []

    # Recopilar resultados de los procesos desde la cola
    while not result_queue.empty():
        max_num, cpu_percent, memory_percent, steps = result_queue.get()
        max_numbers.append(max_num)
        cpu_percentages.append(cpu_percent)
        memory_percentages.append(memory_percent)  # Agregar el porcentaje de memoria a la lista
        steps_per_core.append(steps)

    # Encontrar el máximo de los máximos obtenidos
    overall_max = max(max_numbers)

    # Imprimir resultados por cada núcleo
    for i, (cpu_percent, memory_percent, steps) in enumerate(zip(cpu_percentages, memory_percentages, steps_per_core)):
        print(f"\nCaracterísticas del núcleo {i + 1}:")
        print(f"Uso de CPU: {cpu_percent}%")
        print(f"Uso de memoria: {memory_percent}%")
        print(f"Pasos realizados: {steps}")

    # Imprimir resultados generales
    print("\nCaracterísticas generales del computador:")
    print(f"Número de núcleos de CPU: {cpu_count}")
    print(f"Uso de RAM: {ram_percent}%")
    print("El mayor número encontrado:", overall_max)