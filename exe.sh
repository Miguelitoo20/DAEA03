#!/bin/bash

# Construir la imagen Docker con la etiqueta 'blazor-app'
docker build -t blazor-app .

# Ejecutar el contenedor con el nombre 'blazor-container' y mapear el puerto 5000 en el contenedor al puerto 8080 en el host
docker run --rm -d --name blazor-container -p 8080:5000 blazor-app 

# Ejecutar el script de monitorización
python3 monitor_docker.py
