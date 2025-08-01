# flask-project
# Estructura y Flujo del Proyecto
---

## 1. `run.py`: Punto de entrada

* Carga variables de entorno con `load_dotenv()`.
* Crea la app con `create_app()`.
* Ejecuta el servidor si es ejecutado directamente.

```python
from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

---

## 2. `app/__init__.py`: Creación de la app

* Configura Flask desde `Config`.
* Inicializa extensiones: SQLAlchemy, Migrate.
* Registra Blueprints y manejadores de errores.
* Inicializa logging.

---

## 3. `Config`: Variables y settings

```python
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

---

## 4. `core/db.py`: Extensiones globales

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
```

---

## 5. `model_registry.py`: Registro de modelos

```python
from app.users.models import User
from app.books.models import Book
```

---

## 6. Módulos `users/` y `books/`

Cada módulo contiene:

* `models.py`: Modelos SQLAlchemy.
* `routes.py`: Blueprints con endpoints.
* `schemas.py`: Validación Pydantic.
* `services.py`: Lógica de negocio.

---

## 7. `services.py`: Capa de negocio

Ejemplo:

```python
class UserService:
    @staticmethod
    def get_user_by_id(id):
        return db.session.get(User, id)
```

Ventaja: aislado del framework, testeable y reutilizable.

---

## 8. `schemas.py`: Validaciones Pydantic

```python
class UserCreateSchema(BaseModel):
    username: constr(min_length=1)
    email: EmailStr

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
```

---

## 9. `register_error_handlers()`

```python
@app.errorhandler(UserAlreadyExistsError)
def handle_user_exists(error):
    current_app.logger.error(f"User already exists: {error}")
    return jsonify({"error": "User already exists"}), 409
```

---

## 10. `.env` / `.flaskenv`: Variables de entorno

```env
FLASK_ENV=development
GEMINI_API_KEY=tu_clave
DATABASE_URL=sqlite:///app.db
```

Se carga automáticamente con `flask run` o manualmente con `load_dotenv()`.

---

## 11. Testing (`tests/` + `conftest.py`)

```python
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

Correr tests:

```bash
pytest -v
```

---

## 12. Mocking (con `pytest-mock`)

```python
mocker.patch("app.users.services.UserService.get_user_by_id", return_value=...)
```

---

## 13. Recomendaciones / Gemini

Acceso al API:

```python
from google import genai
client = genai.Client(api_key=GEMINI_API_KEY)
```

Para evitar errores en tests, asegurate de cargar correctamente `.env` o usar mocks.

---

## Estructura del proyecto

```
flask-project/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── db.py
│   │   └── model_registry.py
│   ├── users/
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── services.py
│   └── books/
│       ├── models.py
│       ├── routes.py
│       ├── schemas.py
│       └── services.py
├── tests/
│   ├── test_users.py
│   ├── test_books.py
│   └── conftest.py
├── .env
├── .flaskenv
├── run.py
├── requirements.txt
└── README.md
```

---
