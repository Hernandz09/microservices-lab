# Screenshots - Día 2

Esta carpeta contiene las capturas de pantalla que demuestran el funcionamiento del microservicio de autenticación.

## Archivos requeridos:

1. **day2-register.png** - Captura del endpoint POST /api/register/
   - Muestra el registro exitoso del usuario Pedro@example.com
   - Response 201 Created con datos del usuario

2. **day2-login.png** - Captura del endpoint POST /api/token/
   - Muestra el login exitoso
   - Response 200 OK con tokens access y refresh

3. **day2-me-endpoint.png** - Captura del endpoint GET /api/me/
   - Muestra el perfil del usuario autenticado
   - Header Authorization con Bearer token
   - Response 200 OK con datos del usuario

4. **day2-docker-ps.png** - Captura del comando docker ps
   - Muestra los 3 contenedores corriendo:
     - auth_service (puerto 8000)
     - db_postgres (puerto 5432)
     - cache_redis (puerto 6379)

## Instrucciones:

Por favor, guarda las capturas de Postman y la terminal en esta carpeta con los nombres exactos mencionados arriba para que las referencias en el README principal funcionen correctamente.
