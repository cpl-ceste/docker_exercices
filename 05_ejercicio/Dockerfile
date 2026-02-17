# SOLUCIÓN COMENTADA: Dockerfile Hardening

# 1. Usar imágenes base mínimas (Alpine) reduce la superficie de ataque
FROM python:3.9-alpine

# 2. Crear un grupo y usuario de sistema sin privilegios
# -S: crea un usuario/grupo de sistema
# -D: no asigna password
# -H: no crea home directory
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Instalar dependencias
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app/ .

# 3. Asignar permisos: El usuario root (por defecto en build) copia los archivos, 
# pero debemos cambiar el propietario al usuario no privilegiado para que pueda leerlos/ejecutarlos 
# si fuera necesario escribir (aunque idealmente la app no debería escribir en su propio código).
RUN chown -R appuser:appgroup /app

# 4. Cambiar al usuario no privilegiado
# A partir de esta línea, todas las instrucciones (CMD, RUN, ENTRYPOINT) se ejecutan como este usuario.
# Esto previene que si el contenedor es comprometido, el atacante tenga acceso root dentro del contenedor.
USER appuser

# 5. Exponer un puerto alto (>1024)
# Los puertos < 1024 requieren privilegios de root para ser abiertos. 
# Al usar 8080, permitimos que el usuario 'appuser' pueda iniciar el servicio.
EXPOSE 8080

# Comando de inicio
CMD ["python", "main.py"]
