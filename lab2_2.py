from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Масив даних
X = np.array([3, -2, 5, -1, 7, -3, 8, -6, 2, -5, 4, -8, 9, -7, 1])

# Розподіл завдань між процесами
chunk_size = len(X) // size
remainder = len(X) % size
start_index = rank * chunk_size + min(rank, remainder)
end_index = start_index + chunk_size + (1 if rank < remainder else 0)

# Локальні змінні для підрахунку суми додатних та відʼємних чисел
positive_sum = 0
negative_sum = 0
positive_count = 0
negative_count = 0

# Обчислення локальних сум та кількості додатних і від'ємних елементів
for i in range(start_index, end_index):
    if X[i] > 0:
        positive_sum += X[i]
        positive_count += 1
    elif X[i] < 0:
        negative_sum += X[i]
        negative_count += 1

# Використання секцій для паралельного обчислення середнього
R1 = 0
R2 = 0

if positive_count > 0:
    R1 = positive_sum / positive_count
if negative_count > 0:
    R2 = negative_sum / negative_count

# Збір результатів на процесі 0
R1_all = comm.gather(R1, root=0)
R2_all = comm.gather(R2, root=0)

if rank == 0:
    # Обчислення загального середнього для всіх процесів
    R1_final = sum(R1_all) / size if len(R1_all) > 0 else 0
    R2_final = sum(R2_all) / size if len(R2_all) > 0 else 0

    # Виведення результатів
    print(f"R1 (середнє додатніх елементів): {R1_final}")
    print(f"R2 (середнє відʼємних елементів): {R2_final}")

    if R1_final > R2_final:
        print(f"Середнє додатніх елементів більше: {R1_final}")
    elif R1_final < R2_final:
        print(f"Середнє відʼємних елементів більше: {R2_final}")
    else:
        print("Середнє значення додатніх і відʼємних елементів однакове.")
