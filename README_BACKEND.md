# Backend Biblioteca - FastAPI

Backend para el frontend de biblioteca publicado en:

https://aguayo-0107.github.io/Ej-Codex/

Este backend usa **FastAPI** y almacenamiento **en memoria con Python**, sin base de datos. Los datos se pierden cuando el proceso se reinicia, lo cual es suficiente para una versión demo o educativa.

## Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- CORS habilitado para GitHub Pages

## Modelo de libro

Cada libro tiene la siguiente estructura:

```json
{
  "id": "0f6b7f3d-3a4e-4a4e-8d9e-123456789abc",
  "titulo": "Cien años de soledad",
  "autor": "Gabriel García Márquez",
  "fechaPublicacion": "1967-05-30",
  "cantidad": 3,
  "estado": "disponible"
}
```

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID string | Identificador único generado automáticamente |
| `titulo` | string | Título del libro |
| `autor` | string | Autor del libro |
| `fechaPublicacion` | date | Fecha de publicación |
| `cantidad` | integer | Stock disponible |
| `estado` | enum | `disponible` o `prestado` |

## Endpoints

Base URL local:

```txt
http://localhost:8000
```

Base URL en Render:

```txt
https://TU-SERVICIO.onrender.com
```

### Health check

```http
GET /health
```

Respuesta:

```json
{
  "status": "ok"
}
```

### Obtener libros con filtros y paginación

```http
GET /books
```

Query params disponibles:

| Parámetro | Tipo | Ejemplo | Descripción |
|---|---|---|---|
| `page` | integer | `1` | Página actual |
| `size` | integer | `10` | Cantidad por página |
| `q` | string | `borges` | Búsqueda general por título o autor |
| `titulo` | string | `rayuela` | Filtra por título |
| `autor` | string | `cortazar` | Filtra por autor |
| `estado` | string | `disponible` | Filtra por `disponible` o `prestado` |
| `sort` | string | `titulo_asc` | Orden: `titulo_asc`, `titulo_desc`, `fecha_asc`, `fecha_desc` |

Ejemplo:

```http
GET /books?page=1&size=10&estado=disponible&sort=titulo_asc
```

Respuesta sugerida:

```json
{
  "items": [
    {
      "id": "0f6b7f3d-3a4e-4a4e-8d9e-123456789abc",
      "titulo": "Cien años de soledad",
      "autor": "Gabriel García Márquez",
      "fechaPublicacion": "1967-05-30",
      "cantidad": 3,
      "estado": "disponible"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

### Obtener libro por ID

```http
GET /books/{book_id}
```

### Obtener libros por estado

```http
GET /books/status/{estado}
```

Ejemplos:

```http
GET /books/status/disponible
GET /books/status/prestado
```

También se puede usar el endpoint principal:

```http
GET /books?estado=prestado
```

### Crear libro

```http
POST /books
```

Body:

```json
{
  "titulo": "Rayuela",
  "autor": "Julio Cortázar",
  "fechaPublicacion": "1963-06-28",
  "cantidad": 5,
  "estado": "disponible"
}
```

### Editar libro completo

```http
PUT /books/{book_id}
```

Body:

```json
{
  "titulo": "Rayuela",
  "autor": "Julio Cortázar",
  "fechaPublicacion": "1963-06-28",
  "cantidad": 4,
  "estado": "prestado"
}
```

### Editar libro parcialmente

```http
PATCH /books/{book_id}
```

Ejemplo para marcar como prestado:

```json
{
  "estado": "prestado"
}
```

### Eliminar libro

```http
DELETE /books/{book_id}
```

Respuesta:

```json
{
  "message": "Libro eliminado correctamente"
}
```

### Métricas para la pantalla de inicio

```http
GET /stats
```

Respuesta:

```json
{
  "total": 10,
  "disponibles": 7,
  "prestados": 3,
  "ultimosAgregados": []
}
```

## Estructura

```txt
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── store.py
├── requirements.txt
├── render.yaml
└── README_BACKEND.md
```

## Ejecutar localmente

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar en Linux/macOS:

```bash
source .venv/bin/activate
```

Activar en Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Levantar servidor:

```bash
uvicorn app.main:app --reload
```

Abrir documentación Swagger:

```txt
http://localhost:8000/docs
```

## Conectar con el frontend

En el frontend, define una variable con la URL base del backend.

Producción:

```js
const API_URL = "https://TU-SERVICIO.onrender.com";
```

Local:

```js
const API_URL = "http://localhost:8000";
```

Obtener libros:

```js
fetch(`${API_URL}/books?page=1&size=10&estado=disponible&sort=titulo_asc`)
  .then((res) => res.json())
  .then((data) => console.log(data));
```

Crear libro:

```js
fetch(`${API_URL}/books`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    titulo: "Rayuela",
    autor: "Julio Cortázar",
    fechaPublicacion: "1963-06-28",
    cantidad: 5,
    estado: "disponible"
  })
});
```

Editar libro:

```js
fetch(`${API_URL}/books/${id}`, {
  method: "PATCH",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    estado: "prestado"
  })
});
```

Eliminar libro:

```js
fetch(`${API_URL}/books/${id}`, {
  method: "DELETE"
});
```

## Despliegue en Render

### Dashboard de Render

1. Subir el backend a GitHub.
2. Entrar a <https://render.com>.
3. Crear un nuevo **Web Service**.
4. Conectar el repositorio.
5. Configurar:

```txt
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

6. Deploy.

### Blueprint con `render.yaml`

El archivo `render.yaml` incluido permite desplegar como Blueprint en Render.

## Comandos sugeridos para subir el backend

```bash
git add .
git commit -m "Add FastAPI backend for library"
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git branch -M main
git push -u origin main
```

## Endpoints finales resumidos

| Método | Endpoint | Uso |
|---|---|---|
| `GET` | `/health` | Verificar estado de la API |
| `GET` | `/books` | Listar libros con filtros, orden y paginación |
| `GET` | `/books/{book_id}` | Obtener libro por ID |
| `GET` | `/books/status/{estado}` | Obtener libros por estado |
| `POST` | `/books` | Crear libro |
| `PUT` | `/books/{book_id}` | Reemplazar libro completo |
| `PATCH` | `/books/{book_id}` | Editar libro parcialmente |
| `DELETE` | `/books/{book_id}` | Eliminar libro |
| `GET` | `/stats` | Métricas para la página de inicio |
