from mpi4py import MPI

# Ініціалізація MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Отримання рангу поточного процесу
size = comm.Get_size()  # Отримання загальної кількості процесів

# Якщо це головний процес (ранг 0)
if rank == 0:
    print(f"Hello from the master process (Rank {rank})")
    for i in range(1, size):
        # Отримання рангу від кожного з інших процесів
        received_rank = comm.recv(source=i, tag=0)
        print(f"Received rank {received_rank} from process {i}")
else:
    # Інші процеси надсилають свій ранг головному процесу
    comm.send(rank, dest=0, tag=0)