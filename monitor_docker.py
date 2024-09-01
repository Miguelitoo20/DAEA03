import docker
import psutil  # Librería para obtener estadísticas del sistema
import platform  # Librería para obtener información del sistema
import requests  # Librería para enviar solicitudes HTTP

# Inicializa el cliente Docker
client = docker.from_env()

# Nombre del contenedor y puerto del servicio
container_name = "blazor-container"
service_url = "http://localhost:8080/"  # URL del servicio en el contenedor

# Verifica si el contenedor existe y está en ejecución
try:
    container = client.containers.get(container_name)
except docker.errors.NotFound:
    print(f"Container '{container_name}' not found.")
    client.close()
    exit()

container_status = container.status
print(f"Container Status: {container_status}")

# Verifica si el servicio está funcionando correctamente
if container_status == 'running':
    try:
        response = requests.get(service_url)
        if response.status_code == 200:
            service_status = "Service is running and responding correctly."
        else:
            service_status = f"Service responded with status code {response.status_code}."
    except requests.ConnectionError:
        service_status = "Service is not reachable or not responding."
else:
    service_status = "Container is not running."

# Obtén las estadísticas del contenedor
stats = container.stats(stream=False)

# Cálculo del uso de CPU en porcentaje
cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
number_cpus = stats['cpu_stats']['online_cpus']

if system_delta > 0:
    cpu_usage = (cpu_delta / system_delta) * number_cpus * 100
else:
    cpu_usage = 0

# Cálculo del uso de memoria en porcentaje
memory_usage = stats['memory_stats']['usage']
memory_limit = stats['memory_stats']['limit']
memory_usage_percent = (memory_usage / memory_limit) * 100

# Monitorización del host
cpu_usage_host = psutil.cpu_percent(interval=1)  # Uso de CPU del host en porcentaje
memory_info = psutil.virtual_memory()  # Información de memoria del host
memory_usage_host = memory_info.used
memory_total_host = memory_info.total
memory_usage_percent_host = (memory_usage_host / memory_total_host) * 100

# Información del sistema
system_info = platform.uname()

# Formato legible
print(f"CPU Usage (Container): {cpu_usage:.2f}%")
print(f"Memory Usage (Container): {memory_usage / (1024 ** 2):.2f} MB / {memory_limit / (1024 ** 2):.2f} MB ({memory_usage_percent:.2f}%)")

print(f"\nHost System Information:")
print(f"System: {system_info.system} {system_info.release}")
print(f"Node Name: {system_info.node}")
print(f"Processor: {system_info.processor}")

print(f"\nCPU Usage (Host): {cpu_usage_host:.2f}%")
print(f"Memory Usage (Host): {memory_usage_host / (1024 ** 2):.2f} MB / {memory_total_host / (1024 ** 2):.2f} MB ({memory_usage_percent_host:.2f}%)")

print(f"\nService Status: {service_status}")

# Cierre del cliente Docker
client.close()
