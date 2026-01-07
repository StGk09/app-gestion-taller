# TallerFlow: Sistema de Gestión de Reparaciones Serverless

Un sistema completo de registro de órdenes de servicio, firmas digitales y evidencia fotográfica, desplegado en la nube utilizando arquitectura Serverless.

## Características
- **Interfaz Web Reactiva:** Construida con Streamlit (Python).
- **Almacenamiento Híbrido:** - Datos estructurados en **Google Sheets** (API v4).
  - Evidencia multimedia en **Cloudinary** (CDN).
- **Firmas Digitales:** Captura de firmas de cliente y técnico mediante HTML5 Canvas.
- **Seguridad:** Gestión de credenciales mediante Secrets Management (evitando exposición en código).

## Arquitectura
```
[ Usuario ] --> [ App Streamlit (Python) ]
                      |
                      +---> [ Cloudinary API ] (Sube fotos, retorna URL segura)
                      |
                      +---> [ Google Sheets API ] (Guarda metadatos + URLs)

```

## Instalación y Uso Local

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/app-gestion-taller.git](https://github.com/TU_USUARIO/app-gestion-taller.git)
2. Instalar dependencias:

Bash

pip install -r requirements.txt

3. Configuración de Secretos: Crear carpeta .streamlit/secrets.toml con las credenciales de Google Service Account y Cloudinary API.

4. Ejecutar:
  ```bash
  streamlit run registro_taller.py
  ```

## Seguridad (Hardening)

Este proyecto implementa las siguientes prácticas de seguridad:

OAuth2 Service Accounts: Autenticación robusta server-to-server.

GitIgnore: Exclusión estricta de archivos .toml y caches.

Sanitización: Validación de tipos MIME en subida de archivos.

Capturas de Pantalla
