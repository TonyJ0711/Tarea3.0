# Paso 1: Imagen base
FROM python:3.12-alpine

# Paso 2: Directorio de trabajo
WORKDIR /app

# Paso 3: Copiar dependencias
COPY requeriments.txt /app

# Paso 4: Instalar dependencias
RUN pip install --no-cache-dir -r requeriments.txt

# Paso 5: Copiar código fuente
COPY app.py /app

# Paso 6: Exponer puerto
EXPOSE 5000

# Paso 7: Ejecutar la app
CMD ["python", "app.py"]