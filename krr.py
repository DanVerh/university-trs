from mpi4py import MPI
import datetime
import csv

# ІНІЦІАЛІЗАЦІЯ MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Номер процесу
size = comm.Get_size()  # Загальна кількість процесів

# ВВЕДЕННЯ ПАРАМЕТРІВ
# Приклад даних: масив ділянок
land_data = [
    {"id": 1, "area": 5, "type": "agricultural", "location": "10 km from city"},
    {"id": 2, "area": 3, "type": "commercial", "location": "city center"},
    {"id": 3, "area": 7, "type": "residential", "location": "suburb"},
]

# РОЗРАХУНОК ЦІНИ
# Функція для обчислення ціни
def calculate_price(area, land_type, location):
    base_price = 1000
    type_coeff = {"agricultural": 0.8, "commercial": 1.5, "residential": 1.2}
    location_coeff = {"10 km from city": 1.2, "city center": 2.0, "suburb": 1.0}
    return area * base_price * type_coeff[land_type] * location_coeff[location]

# Розподіл даних між процесами
if rank == 0:
    # Головний вузол ділить дані
    chunks = [land_data[i::size] for i in range(size)]
else:
    chunks = None

# Передача даних кожному вузлу
local_data = comm.scatter(chunks, root=0)

# Обробка даних на кожному вузлі
local_results = []
for land in local_data:
    price = calculate_price(land["area"], land["type"], land["location"])
    land["price"] = price
    land["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    local_results.append(land)

# Збирання результатів у головному вузлі
all_results = comm.gather(local_results, root=0)

if rank == 0:
    # ФОРМУВАННЯ УГОДИ
    # Об'єднання результатів
    final_results = [item for sublist in all_results for item in sublist]

    # ГЕНЕРАЦІЯ ЗВІТУ
    with open("transactions_report.csv", "w", newline="") as csvfile:
        fieldnames = ["ID", "Дата", "Площа (га)", "Тип", "Розташування", "Ціна (USD)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # ВИВЕДЕННЯ РЕЗУЛЬТАТІВ
        writer.writeheader()  # Запис заголовків
        for land in final_results:
            writer.writerow({
                "ID": land["id"],
                "Дата": land["date"],
                "Площа (га)": land["area"],
                "Тип": land["type"],
                "Розташування": land["location"],
                "Ціна (USD)": land["price"],
            })