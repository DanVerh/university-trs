import concurrent.futures


# Функція для обчислення x
def calculate_x(y1, y2, y3, y1_prime, y2_prime):
    term1 = y3 * (y2 ** 2) * y2_prime
    term2 = (y3 ** 3) - y3
    term3 = y2 * y1_prime + (y3 ** 2) * y1 * y1_prime
    x = term1 + term2 + term3
    return x


# Функція для обчислення b_i
def calculate_b(i):
    if i % 2 == 0:  # Парні i
        return 3 / (i ** 2 + 3)
    else:  # Непарні i
        return 3 / i


# Функція для обчислення A1(3b1 + c1)
def calculate_A1(b1, c1, A1):
    return A1 * (3 * b1 + c1)


# Функція для обчислення A2(B2 - C2)
def calculate_A2(B2, C2, A2):
    return A2 * (B2 - C2)


# Функція для обчислення C_ij
def calculate_C(i, j):
    return 1 / ((i + j) ** 2)


# Головна функція для обчислення всіх значень паралельно
def main(y1, y2, y3, y1_prime, y2_prime, A1, A2, B2, C2):
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Виконуємо обчислення паралельно
        future_x = executor.submit(calculate_x, y1, y2, y3, y1_prime, y2_prime)
        future_b1 = executor.submit(calculate_b, 1)
        future_A1 = executor.submit(calculate_A1, future_b1.result(), C2, A1)
        future_A2 = executor.submit(calculate_A2, B2, C2, A2)
        future_Cij = {
            (i, j): executor.submit(calculate_C, i, j)
            for i in range(1, 4)
            for j in range(1, 4)
        }

        # Збираємо результати
        results["x"] = future_x.result()
        results["b1"] = future_b1.result()
        results["A1"] = future_A1.result()
        results["A2"] = future_A2.result()
        results["Cij"] = {
            (i, j): future.result() for (i, j), future in future_Cij.items()
        }
    return results


# Функція для виводу результатів
def print_results(results):
    print("Результати обчислень:")
    print(f"x = {results['x']:.4f}")
    print(f"b1 = {results['b1']:.4f}")
    print(f"A1(3b1 + c1) = {results['A1']:.4f}")
    print(f"A2(B2 - C2) = {results['A2']:.4f}")
    print("Матриця C_ij:")
    for (i, j), value in results["Cij"].items():
        print(f"C({i},{j}) = {value:.4f}")
    print("\n")


# Вхідні дані
y1, y2, y3 = 1, 2, 3
y1_prime, y2_prime = 4, 5
A1, A2, B2, C2 = 7, 8, 9, 10


# Виклик функції
results = main(y1, y2, y3, y1_prime, y2_prime, A1, A2, B2, C2)
print_results(results)
