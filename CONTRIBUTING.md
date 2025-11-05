# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a Microservices Lab! Este documento te guiará en el proceso.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)

## 📜 Código de Conducta

Este proyecto y todos sus participantes están sujetos a un código de conducta. Al participar, se espera que mantengas este código. Por favor reporta comportamientos inaceptables.

## 🚀 Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no haya sido reportado previamente
2. Abre un issue describiendo:
   - Pasos para reproducir
   - Comportamiento esperado vs. actual
   - Capturas de pantalla (si aplica)
   - Versiones de Docker, Python, etc.

### Sugerir Mejoras

1. Abre un issue con la etiqueta `enhancement`
2. Describe claramente la funcionalidad propuesta
3. Explica por qué sería útil

### Contribuir con Código

1. **Fork** el repositorio
2. **Crea una rama** desde `main`:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   # o
   git checkout -b fix/correccion-bug
   ```
3. **Realiza tus cambios**
4. **Commitea** con mensajes descriptivos
5. **Push** a tu fork
6. **Abre un Pull Request**

## 🛠️ Configuración del Entorno

### Requisitos Previos

- Docker Desktop 4.0+
- Docker Compose 3.9+
- Git
- Python 3.11+ (para desarrollo local opcional)

### Instalación

```bash
# Clonar tu fork
git clone https://github.com/TU-USUARIO/microservices-lab.git
cd microservices-lab

# Configurar upstream
git remote add upstream https://github.com/Hernandz09/microservices-lab.git

# Copiar variables de entorno
cp .env.example .env

# Levantar servicios
docker compose up -d

# Verificar que todo funciona
docker ps
```

### Desarrollo Local (Opcional)

Si prefieres trabajar sin Docker:

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias de un servicio
cd auth-service
pip install -r requirements.txt

# Configurar variables de entorno locales
export DB_HOST=localhost
export DB_NAME=main_db
# ... etc

# Ejecutar migraciones
python manage.py migrate

# Levantar servidor de desarrollo
python manage.py runserver 8000
```

## 📝 Estándares de Código

### Python (Django/DRF)

- **Estilo**: PEP 8
- **Líneas**: Máximo 100 caracteres
- **Imports**: Organizados (stdlib → third-party → local)
- **Docstrings**: Google style para funciones complejas

```python
# ✅ Bueno
def calculate_total(items: list[dict]) -> float:
    """
    Calculate the total price of items.
    
    Args:
        items: List of dictionaries with 'price' key
        
    Returns:
        Total price as float
    """
    return sum(item['price'] for item in items)

# ❌ Malo
def calc(x):
    return sum(i['price'] for i in x)
```

### Commits

Usa mensajes descriptivos siguiendo [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Formato
<type>(<scope>): <description>

# Ejemplos
feat(auth): add password reset endpoint
fix(blog): resolve pagination bug in posts list
docs(readme): update installation instructions
refactor(email): optimize celery task queue
test(auth): add unit tests for registration
chore(docker): update postgres to v16
```

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato (no afecta código)
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Tareas de mantenimiento

### Estructura de Archivos

```
service-name/
├── service_name/           # Proyecto Django
│   ├── settings.py
│   └── urls.py
├── app_name/              # Django app
│   ├── models.py          # Modelos
│   ├── serializers.py     # Serializadores DRF
│   ├── views.py           # Vistas/ViewSets
│   ├── urls.py            # Rutas
│   ├── admin.py           # Admin
│   └── tests/             # Tests organizados
│       ├── test_models.py
│       ├── test_views.py
│       └── test_serializers.py
├── Dockerfile
├── requirements.txt
├── openapi.yaml           # Contrato API
└── README.md
```

## 🔄 Proceso de Pull Request

### Antes de Crear el PR

- [ ] Tu código sigue los estándares de estilo
- [ ] Has actualizado la documentación (README, OpenAPI)
- [ ] Has agregado tests (si aplica)
- [ ] Todos los tests pasan
- [ ] Los contenedores se construyen sin errores
- [ ] Has actualizado el CHANGELOG (si aplica)

### Checklist del PR

```markdown
## Descripción
Descripción clara de los cambios realizados.

## Tipo de cambio
- [ ] Bug fix (cambio que corrige un issue)
- [ ] Nueva funcionalidad (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que rompe compatibilidad)
- [ ] Documentación

## Checklist
- [ ] Mi código sigue los estándares del proyecto
- [ ] He realizado una auto-revisión
- [ ] He comentado código complejo
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan warnings
- [ ] He agregado tests
- [ ] Los tests nuevos y existentes pasan

## Pruebas Realizadas
Describe las pruebas que realizaste.

## Capturas de Pantalla (si aplica)
Agrega capturas si hay cambios visuales.
```

### Revisión

1. Un maintainer revisará tu PR
2. Puede solicitar cambios
3. Una vez aprobado, será merged a `main`
4. Tu contribución aparecerá en el siguiente release

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests de un servicio específico
docker compose exec auth python manage.py test

# Con coverage
docker compose exec auth coverage run --source='.' manage.py test
docker compose exec auth coverage report

# Tests end-to-end con Postman
newman run postman_collection.json
```

### Escribir Tests

```python
# auth-service/users/tests/test_views.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserRegistrationTests(APITestCase):
    def test_register_user_success(self):
        """Test successful user registration"""
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
```

## 📚 Recursos

- [Documentación de Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## ❓ Preguntas

Si tienes preguntas, puedes:
- Abrir un issue con la etiqueta `question`
- Contactar a [@Hernandz09](https://github.com/Hernandz09)

---

¡Gracias por contribuir! 🎉
