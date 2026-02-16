# User Management System

A RESTful user management API built with **FastAPI**, featuring JWT authentication, password hashing with bcrypt, and PostgreSQL/SQLite support.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **User registration** with email, username, and strong password validation (uppercase, lowercase, digit, special character)
- **JWT-based authentication** (login returns Bearer token)
- **Protected routes** – list users, get user by ID, get current user (`/me`), update and delete require valid token
- **User CRUD** – create, read, update, delete users
- **Password hashing** with bcrypt
- **Pydantic** request/response validation and settings
- **SQLAlchemy** ORM with configurable database (PostgreSQL or SQLite via `DATABASE_URL`)

---

## Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Framework   | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM         | SQLAlchemy 2.x                      |
| Database    | PostgreSQL (production) / SQLite (dev) |
| Auth        | JWT (python-jose), OAuth2 password bearer |
| Password    | bcrypt                              |
| Validation  | Pydantic v2, Pydantic Settings      |
| Server      | Uvicorn                             |
| Package mgr | [uv](https://github.com/astral-sh/uv) (optional) / pip |

---

## Prerequisites

- **Python 3.14+** (see [`.python-version`](.python-version))
- **PostgreSQL** (optional for local dev; SQLite works with a file URL)
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip` and `venv`

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/roopnsingh/user-management-system.git
cd user-management-system
```

### 2. Create a virtual environment (if not using uv)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

**Using uv (recommended):**

```bash
uv sync
```

**Using pip:**

```bash
pip install -e .
# or: pip install -r requirements.txt  # if you generate one from pyproject.toml
```

---

## Configuration

Create a `.env` file in the project root (see [`.gitignore`](.gitignore) – `.env` is not committed):

| Variable                   | Description                          | Example                    |
|---------------------------|--------------------------------------|----------------------------|
| `DATABASE_URL`            | Database connection URL              | `postgresql://user:pass@localhost/dbname` or `sqlite:///./app.db` |
| `SECRET_KEY`              | Secret for JWT signing               | Long random string         |
| `ALGORITHM`               | JWT algorithm (optional)             | `HS256`                    |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime (optional) | `30`                       |

**Example `.env`:**

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Running the Application

Start the server with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **API base:** `http://localhost:8000`
- **Interactive docs (Swagger):** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

Root endpoint:

```bash
curl http://localhost:8000/
# {"message":"Hi!! Welcome to User Management System"}
```

---

## API Documentation

Once the app is running:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs) – try endpoints and authorize with JWT.
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc) – readable API reference.

To use protected endpoints in Swagger, call `POST /api/users/login`, copy the `access_token`, then click **Authorize** and enter: `Bearer <access_token>`.

---

## API Endpoints

All user endpoints are under `/api/users`.

| Method | Endpoint                      | Auth required | Description                |
|--------|-------------------------------|---------------|----------------------------|
| `POST` | `/api/users/register`        | No            | Register a new user        |
| `POST` | `/api/users/login`           | No            | Login; returns JWT         |
| `GET`  | `/api/users/me`              | Yes           | Current user profile       |
| `GET`  | `/api/users/`                | Yes           | List users (paginated)     |
| `GET`  | `/api/users/{user_id}`       | Yes           | Get user by ID             |
| `PUT`  | `/api/users/user_update/{user_id}` | Yes    | Update user                |
| `DELETE` | `/api/users/delete/{user_id}` | Yes         | Delete user                |

**Auth:** Send the JWT in the header: `Authorization: Bearer <access_token>`.

---

## Project Structure

```
user-management-system/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependency injection (DB session, current user, OAuth2)
│   │   └── v1/
│   │       └── endpoints/
│   │           └── users.py     # User routes (register, login, CRUD, /me)
│   ├── core/
│   │   ├── config.py           # Pydantic settings (env)
│   │   └── security.py        # JWT creation, bcrypt hash/verify
│   ├── db/
│   │   ├── base.py            # SQLAlchemy declarative base
│   │   └── session.py         # Engine and session factory
│   ├── models/
│   │   └── user.py            # User SQLAlchemy model
│   ├── schemas/
│   │   └── user.py            # Pydantic schemas (User, UserCreate, Token, etc.)
│   ├── services/
│   │   └── user.py            # User business logic (CRUD, auth)
│   └── main.py                # FastAPI app, router includes, DB table creation
├── .env                        # Local config (not committed)
├── .gitignore
├── .python-version             # 3.14
├── pyproject.toml              # Project metadata and dependencies
├── README.md
└── uv.lock                     # Lock file (when using uv)
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a Pull Request.

---

## License

This project is open source.
