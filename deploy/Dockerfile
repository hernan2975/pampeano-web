FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no root
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Copiar y instalar dependencias
COPY --chown=app:app requirements.txt .
RUN pip install --user -r requirements.txt

# Copiar aplicación
COPY --chown=app:app . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
