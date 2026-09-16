# 📝 ToDo App

A RESTful task management API built with **Django REST Framework**, designed with a clean backend architecture and support for authentication, filtering, API documentation, background task processing, and Dockerized development.

## ✨ Features

* 🔐 JWT-based authentication
* ✅ Task management through a REST API
* 🔎 Filtering support with `django-filter`
* 📚 OpenAPI / Swagger API documentation
* 📧 Email template support
* ⚡ Asynchronous background tasks with Celery
* 🔄 Scheduled tasks with Celery Beat
* 🚀 Redis integration for background task processing
* 🐳 Docker and Docker Compose support
* 🧪 Automated testing with Pytest
* 🧹 Code formatting and quality tools with Black and Flake8

## 🛠 Tech Stack

| Category          | Technologies           |
| ----------------- | ---------------------- |
| Language          | Python 3.11            |
| Framework         | Django 5.2.14          |
| API               | Django REST Framework  |
| Authentication    | JWT / SimpleJWT        |
| API Documentation | drf-spectacular        |
| Filtering         | django-filter          |
| Background Tasks  | Celery                 |
| Message Broker    | Redis                  |
| Scheduled Tasks   | django-celery-beat     |
| Email             | django-mail-templated  |
| Testing           | Pytest, pytest-django  |
| Code Quality      | Black, Flake8          |
| Containerization  | Docker, Docker Compose |

## 🏗 Architecture

The project is structured around a Django backend and supporting services:

```text
ToDo-App/
├── core/                   # Django project
├── .github/
│   └── workflows/          # GitHub Actions workflows
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── LICENSE
```

The Docker Compose environment includes:

```text
                    ┌──────────────┐
                    │    Client    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Django    │
                    │   REST API   │
                    └──────┬───────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      ┌──────────────┐            ┌──────────────┐
      │    Redis     │            │    Email     │
      │    Broker    │            │   smtp4dev   │
      └──────┬───────┘            └──────────────┘
             │
       ┌─────┴─────┐
       ▼           ▼
┌────────────┐ ┌────────────┐
│   Celery   │ │   Celery   │
│   Worker   │ │    Beat    │
└────────────┘ └────────────┘
```

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

* Docker
* Docker Compose
* Git

### 1. Clone the repository

```bash
git clone https://github.com/mohamad-karimi/ToDo-App.git
cd ToDo-App
```

### 2. Configure environment variables

Create a `.env` file in the project root and provide the environment variables required by the Django application.

### 3. Build and start the services

```bash
docker compose up --build
```

### 4. Available services

After starting the project:

| Service         |   Port |
| --------------- | -----: |
| Django API      | `8000` |
| Redis           | `6379` |
| smtp4dev Web UI | `5000` |

The Celery worker and Celery Beat services run as separate containers through Docker Compose.

## 🧪 Testing

Run the test suite inside the backend container:

```bash
docker compose exec backend pytest
```

## 🧹 Code Quality

Format the project with Black:

```bash
black .
```

Run Flake8:

```bash
flake8 .
```

## 📚 API Documentation

The project uses **drf-spectacular** to generate OpenAPI documentation for the REST API.

This makes the API easier to explore, test, and integrate with other clients.

## 📦 Background Processing

Celery is used for asynchronous background processing, with Redis acting as the message broker.

The project also includes **Celery Beat** for scheduled tasks, allowing recurring jobs to be managed alongside the Django application.

## 🐳 Docker

The application is fully containerized for development.

Docker Compose manages the main application and supporting services, making it possible to start the complete development environment with a single command:

```bash
docker compose up --build
```

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for more information.

## 👨‍💻 Author

**Mohamad Karimi**

GitHub: [@mohamad-karimi](https://github.com/mohamad-karimi)
