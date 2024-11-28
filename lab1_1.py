from mpi4py import MPI

# Отримуємо поточний процес і кількість процесів
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Ранг поточного процесу
size = comm.Get_size()  # Загальна кількість процесів

# Визначимо простий обмін повідомленнями між процесами
if rank == 0:
    message = "Hello from process 0"
    print(f"Process {rank} sending message: {message}")
    # Надсилаємо повідомлення процесу 1
    comm.send(message, dest=1, tag=0)
    # Отримуємо повідомлення від процесу 2
    message = comm.recv(source=2, tag=1)
    print(f"Process {rank} received message: {message}")

elif rank == 1:
    # Отримуємо повідомлення від процесу 0
    message = comm.recv(source=0, tag=0)
    print(f"Process {rank} received message: {message}")
    # Надсилаємо повідомлення процесу 2
    comm.send("Hello from process 1", dest=2, tag=1)

elif rank == 2:
    # Отримуємо повідомлення від процесу 1
    message = comm.recv(source=1, tag=1)
    print(f"Process {rank} received message: {message}")
    # Надсилаємо повідомлення процесу 0
    comm.send("Hello from process 2", dest=0, tag=1)