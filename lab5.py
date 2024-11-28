import concurrent.futures


# Функція для порівняння та перестановки двох чисел
def compare_and_swap(x, y):
    if x > y:
        return y, x
    return x, y


# Паралельний алгоритм сортування п'яти чисел
def sort_five_numbers_parallel(a, b, c, d, e):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Виконуємо перший набір порівнянь
        a, b = executor.submit(compare_and_swap, a, b).result()
        c, d = executor.submit(compare_and_swap, c, d).result()

        # Порівнюємо середні елементи з різних груп
        b, d = executor.submit(compare_and_swap, b, d).result()

        # Порівнюємо мінімальні елементи
        a, c = executor.submit(compare_and_swap, a, c).result()

        # Порівнюємо максимальне значення з останнім числом
        b, e = executor.submit(compare_and_swap, b, e).result()
        c, e = executor.submit(compare_and_swap, c, e).result()

        # Завершальні порівняння для впорядкування
        b, c = executor.submit(compare_and_swap, b, c).result()

    return [a, b, c, d, e]


# Головна функція для вводу та виводу результатів
def main():
    print("Введіть п'ять попарно різних цілих чисел:")
    a = int(input("a: "))
    b = int(input("b: "))
    c = int(input("c: "))
    d = int(input("d: "))
    e = int(input("e: "))

    # Сортуємо числа
    sorted_numbers = sort_five_numbers_parallel(a, b, c, d, e)
    print("Впорядковані числа:", sorted_numbers)


if __name__ == "__main__":
    main()
