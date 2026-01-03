# 1. Usamos una imagen base oficial de Python (ligera y segura)
FROM python:3.9-slim

# 2. Metadatos del proyecto
LABEL maintainer="BioTwin-Org"
LABEL description="Digital Twin Engine powered by NVIDIA BioNeMo"

# 3. Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Importante: Añadir /app al path para que Python encuentre tus módulos 'src'
ENV PYTHONPATH=/app

# 4. Crear directorio de trabajo dentro del contenedor
WORKDIR /app

# 5. Instalar dependencias del sistema (necesario para algunas librerías científicas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 6. Copiar dependencias e instalarlas (Aprovechando caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copiar el código fuente del proyecto
COPY . .

# 8. Comando por defecto: Ejecutar el Orquestador
CMD ["python", "src/core_orchestrator/main.py"]
