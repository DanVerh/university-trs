import math
import multiprocessing

# Функція для обчислення значення підінтегральної функції
def f(x):
    return (math.exp(x) - 1) * math.exp(x)

# Функція для обчислення частини інтегралу на кожному процесі
def partial_integral(start, end, step):
    local_sum = 0.0
    for i in range(start, end):
        x = (i + 0.5) * step  # Центр кожного підінтервалу
        local_sum += f(x)
    return local_sum

def main():
    a = 0.0  # Початок інтеграції
    b = 1.0  # Кінець інтеграції
    N = 1000000  # Кількість підінтервалів
    step = (b - a) / N  # Крок інтегрування

    # Кількість процесів
    num_processes = multiprocessing.cpu_count()

    # Розподіляємо роботу на декілька процесів
    chunk_size = N // num_processes
    pool = multiprocessing.Pool(processes=num_processes)

    # Створюємо списки для передачі кожному процесу
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    ranges[-1] = (ranges[-1][0], N)  # Останній процес може обробляти більше

    # Паралельне обчислення часткових інтегралів
    local_sums = pool.starmap(partial_integral, [(start, end, step) for start, end in ranges])

    # Підсумовуємо всі локальні результати
    integral = sum(local_sums) * step

    print(f"Обчислений інтеграл: {integral:.10f}")

if __name__ == "__main__":
    main()
