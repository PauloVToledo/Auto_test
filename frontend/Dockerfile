# 1. Usamos una imagen de Nginx ultraligera (Alpine Linux)
FROM nginx:alpine

# 2. Borramos la configuración por defecto de Nginx (opcional, buena práctica)
RUN rm -rf /usr/share/nginx/html/*

# 3. Copiamos TUS archivos (index.html, style.css, app.js) a la carpeta pública de Nginx
COPY . /usr/share/nginx/html

# 4. Exponemos el puerto 80 (el puerto estándar web dentro del contenedor)
EXPOSE 80

# 5. Nginx se inicia automáticamente, no necesitamos CMD