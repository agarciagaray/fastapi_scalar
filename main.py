from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
# ... existing code ...
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

# Intentar importar Scalar de forma segura (puede no estar instalado)
try:
    from scalar_fastapi import get_scalar_api_reference
    try:
        from scalar_fastapi import ScalarTheme  # Puede no existir según la versión
    except Exception:
        ScalarTheme = None
    _SCALAR_AVAILABLE = True
except Exception:
    get_scalar_api_reference = None
    ScalarTheme = None
    _SCALAR_AVAILABLE = False

# --- Definición de la app ---
app = FastAPI(
    title="Mi API Profesional 🚀",
    description="Documentación con **Swagger, ReDoc y Scalar**",
    version="1.0.0",
    contact={
        "name": "Alejandro García",
        "url": "https://www.igdsas.com.co",
        "email": "soporte@igdsas.com.co",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
)

# --- Modelos ---
class Item(BaseModel):
    id: int
    name: str
    price: float

# --- Endpoints ---
@app.get("/items", response_model=list[Item], tags=["Items"])
def list_items():
    return [
        {"id": 1, "name": "Laptop", "price": 1200},
        {"id": 2, "name": "Mouse", "price": 25.5},
    ]

@app.post("/items", response_model=Item, tags=["Items"])
def create_item(item: Item):
    return item

# --- Documentación Swagger ---
@app.get("/swagger", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Swagger UI - Docs"
    )

# --- Documentación ReDoc ---
@app.get("/redoc", include_in_schema=False)
async def redoc_ui():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="ReDoc - Docs"
    )

# --- Documentación Scalar ---
# Intentar usar el Enum de tema si está disponible; de lo contrario, omitir el parámetro.
try:
    from scalar_fastapi import ScalarTheme  # Puede no existir según la versión
    THEME_VALUE = getattr(ScalarTheme, "PURPLE", None) or getattr(ScalarTheme, "purple", None)
except Exception:
    THEME_VALUE = None

# Construcción robusta de kwargs para evitar pasar un str en 'theme'
_scalar_kwargs = {
    "openapi_url": app.openapi_url,
    "title": "📖 API Docs - Scalar",
    "hide_client_button": False,
    "hide_download_button": False,
}
if THEME_VALUE is not None:
    _scalar_kwargs["theme"] = THEME_VALUE

if _SCALAR_AVAILABLE and get_scalar_api_reference is not None:
    app.mount(
        "/docs",
        get_scalar_api_reference(
            **_scalar_kwargs
        ),
        name="scalar-docs",
    )
# Fallback: si Scalar no está disponible, exponer Swagger en /docs
else:
    @app.get("/docs", include_in_schema=False)
    async def docs_fallback():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title="Swagger UI - Docs"
        )

# --- Landing con selector de documentaciones ---
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>📚 Documentación de la API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                background: white;
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            h1 {
                margin-bottom: 1rem;
                color: #4a148c;
            }
            a {
                display: block;
                margin: 0.5rem 0;
                padding: 0.8rem 1.2rem;
                border-radius: 12px;
                text-decoration: none;
                font-weight: bold;
                transition: 0.3s;
            }
            a.scalar { background: #7e57c2; color: white; }
            a.scalar:hover { background: #5e35b1; }
            a.swagger { background: #2e7d32; color: white; }
            a.swagger:hover { background: #1b5e20; }
            a.redoc { background: #1565c0; color: white; }
            a.redoc:hover { background: #0d47a1; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 Documentación de la API</h1>
            <a href="/docs" class="scalar">✨ Scalar (Recomendada)</a>
            <a href="/swagger" class="swagger">⚡ Swagger UI</a>
            <a href="/redoc" class="redoc">📘 ReDoc</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
