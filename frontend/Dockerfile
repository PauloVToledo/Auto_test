# Usamos Nginx Alpine (muy ligero, pesa menos de 10MB)
FROM nginx:alpine

# (Opcional) Borrar la página de bienvenida por defecto de Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copiamos tus archivos (index.html, style.css, app.js, imágenes)
# a la carpeta pública de Nginx
COPY . /usr/share/nginx/html

# Exponemos el puerto 80 (el estándar web)
EXPOSE 80

# Nginx se inicia solo, no hace falta CMD