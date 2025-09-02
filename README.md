# README.md

## Descripción

Este ejemplo muestra cómo crear una API con FastAPI que expone endpoints simples y ofrece múltiples opciones de documentación interactiva:

- Swagger UI
- ReDoc
- Scalar (si está disponible, con fallback automático a Swagger)

Incluye una página de inicio (landing) que actúa como selector para abrir cualquiera de las tres interfaces de documentación.

La API expone un recurso “Items” con operaciones de lectura y creación para ilustrar el uso de modelos con Pydantic y respuestas tipadas.

---

## Características clave

- FastAPI con metadatos profesionales (título, descripción, contacto, licencia, versión).
- Documentación en tres sabores:
  - Rutas dedicadas: 
    - Scalar en /docs (o fallback a Swagger si Scalar no está disponible).
    - Swagger en /swagger.
    - ReDoc en /redoc.
  - Página de inicio en / con enlaces a cada documentación.
- Endpoints de ejemplo para gestionar “Items”:
  - GET /items: Lista de items.
  - POST /items: Crea un item y devuelve el payload validado.
- Manejo robusto de importación condicional de Scalar para no romper la app si el paquete no está instalado o si cambió la API del tema.
- OpenAPI servido en /openapi.json.

---

## Requisitos

- Python 3.13.7 (o compatible con 3.13.x).
- virtualenv para aislar el entorno de ejecución.
- pip (gestor de paquetes ya disponible en el entorno virtual).

---

## Instalación

1) Crear y activar un entorno virtual

```shell script
# Crear entorno virtual
python3 -m venv .venv

# Activar en Linux/Mac
source .venv/bin/activate

# Activar en Windows (PowerShell)
.venv\Scripts\Activate.ps1
```


2) Instalar dependencias

Las dependencias mínimas para ejecutar la API y la documentación básica son:

```shell script
pip install fastapi uvicorn
```


Dependencia opcional para documentación Scalar:

```shell script
pip install scalar-fastapi
```


Nota: Si no instalas scalar-fastapi, la ruta /docs seguirá funcionando gracias al fallback automático a Swagger UI.

---

## Ejecución

Con el entorno virtual activado:

```shell script
uvicorn main:app --reload
```


Por defecto, la aplicación quedará accesible en:
- http://127.0.0.1:8000

---

## Navegación y documentación

- Página de bienvenida (selector de docs): http://127.0.0.1:8000/
- Scalar (recomendada, si está instalada): http://127.0.0.1:8000/docs
- Swagger UI: http://127.0.0.1:8000/swagger
- ReDoc: http://127.0.0.1:8000/redoc
- Especificación OpenAPI: http://127.0.0.1:8000/openapi.json

Comportamiento con Scalar:
- Si scalar-fastapi está instalado y es compatible, /docs mostrará la UI de Scalar.
- Si no está instalado o falla la importación, /docs servirá automáticamente Swagger UI (fallback).

---

## Endpoints principales

- GET /items
  - Devuelve una lista de items de ejemplo.
- POST /items
  - Recibe un objeto Item y lo devuelve validado.

Modelo Item (campos):
- id: int
- name: str
- price: float

---

## Pruebas rápidas con cURL

- Obtener items

```shell script
curl -X GET http://127.0.0.1:8000/items
```


- Crear un item

```shell script
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"id": 3, "name": "Teclado", "price": 45.99}'
```


---

## Desarrollo

Sugerencias:
- Ejecuta Uvicorn con --reload para recarga en caliente durante el desarrollo.
- Si actualizas dependencias, considera bloquear versiones compatibles en un requirements.txt.
- Para revisar la especificación OpenAPI generada por FastAPI, abre /openapi.json.

---

## Resolución de problemas

- Error de importación de Scalar o temas:
  - Asegúrate de tener scalar-fastapi instalado:
```shell script
pip install scalar-fastapi
```

  - Si continúa fallando, verifica la versión del paquete. En caso de incompatibilidad, la app hará fallback a Swagger automáticamente en /docs.

- No carga la página de documentación:
  - Confirma que la app está corriendo (Uvicorn en el puerto 8000).
  - Revisa que no haya otro proceso usando el puerto:
```shell script
lsof -i :8000   # Linux/Mac
    netstat -ano | findstr :8000   # Windows
```


- Problemas con validación de datos al hacer POST /items:
  - Asegúrate de enviar JSON válido con los campos id (int), name (str) y price (float).

---

## Licencia

MIT License. Consulta el archivo de licencia correspondiente si aplica.

---

## Autor

- Nombre: Alejandro García
- Sitio: https://www.igdsas.com.co
- Email: soporte@igdsas.com.co

---

## Créditos

- FastAPI para el framework de la API.
- Swagger UI, ReDoc y Scalar para la visualización de la documentación OpenAPI.

Si deseas personalizar los estilos, el título o los metadatos de la API, ajusta los parámetros de inicialización de la aplicación y los constructores de las UIs de documentación. Si requieres más endpoints o esquemas, extiende los modelos y rutas según tus necesidades.