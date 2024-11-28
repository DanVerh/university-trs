from mpi4py import MPI
import math

# Функція для обчислення значення підінтегральної функції
def f(x):
    return (math.exp(x) - 1) * math.exp(x)

# Основна функція
def main():
    # Ініціалізація MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Кількість підінтервалів
    N = 1000000
    a = 0.0  # Початок інтеграції
    b = 1.0  # Кінець інтеграції
    step = (b - a) / N  # Крок інтегрування

    # Розподіляємо інтервали між процесами
    local_sum = 0.0
    local_N = N // size  # Кількість елементів на процес

    # Кожен процес обчислює свою частину інтегралу
    for i in range(rank * local_N, (rank + 1) * local_N):
        x = (i + 0.5) * step  # Центр підінтервалу
        local_sum += f(x)

    # Збираємо всі часткові суми
    total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

    # Головний процес виводить результат
    if rank == 0:
        integral = total_sum * step
        print(f"Обчислений інтеграл: {integral:.10f}")

if __name__ == "__main__":
    main()
