# Janitri Backend — Django + DRF

This project implements a backend API for managing **patients** and their **heart-rate records**, with user authentication and JWT tokens.

---

## Features
- **User Registration & Login** with JWT (`djangorestframework-simplejwt`)
- **Patients**: Create, list (with search & ordering), retrieve
- **Heart-Rate Records**: Add & list (with validation, filtering, pagination)
- **Swagger UI**: Interactive API docs at `/api/schema/swagger-ui/`
- Unit tests included for key functionality

---

## Tech Stack
- Python 3.12+
- Django 5.2+
- Django REST Framework 3.16+
- drf-spectacular (Swagger/OpenAPI)
- Simple JWT authentication

---

## Quick Start

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd janitri-backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment
Copy `.env.example` to `.env` and set values:
```
DJANGO_SECRET=your-secret-key
DEBUG=True
```

### 3. Migrate & Run
```bash
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```
The server will run at **http://127.0.0.1:8000/**.

---

## API Endpoints

### Auth
| Method | URL                          | Description               |
|--------|------------------------------|---------------------------|
| POST   | `/api/auth/register/`        | Register a new user       |
| POST   | `/api/auth/token/`           | Obtain JWT access/refresh |
| POST   | `/api/auth/token/refresh/`   | Refresh JWT access token  |

### Patients
| Method | URL                   | Description                     |
|--------|-----------------------|----------------------------------|
| GET    | `/api/patients/`      | List patients (search, ordering) |
| POST   | `/api/patients/`      | Create a patient                 |
| GET    | `/api/patients/<id>/` | Retrieve a patient               |

### Heart-Rate
| Method | URL                                   | Description                                   |
|--------|---------------------------------------|-----------------------------------------------|
| POST   | `/api/heart-rate/`                    | Create a heart-rate record                    |
| GET    | `/api/heart-rate/list/?patient=<id>`  | List heart-rate records (ordering, search)    |

### Docs
- Swagger UI: **`/api/schema/swagger-ui/`**
- OpenAPI schema (JSON): **`/api/schema/`**

---

## Running Tests
Run all included tests:

```bash
python manage.py test
```

---

## Notes
- Default database is SQLite; update `settings.py` for PostgreSQL or others if desired.
- Non-staff users can access only their own patients and readings.
- Heart-rate `bpm` must be between **20 and 250**.

---