# Usamos una imagen ligera de Python
FROM python:3.11-slim

WORKDIR /app

# Copiamos requirements e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código
COPY ./app ./app

# Exponemos el puerto
EXPOSE 8000

# Ejecutamos
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]