# Automotora Management System

This project is a full-stack web application designed for car dealerships to manage vehicle stock and facilitate customer appointment scheduling. It combines a high-performance FastAPI backend with a lightweight frontend interface.

## 🚀 Features

- **Vehicle Catalog**: Display available cars with details such as brand, model, and price.
- **Appointment Booking**: Allow customers to schedule visits to inspect specific vehicles.
- **WhatsApp Integration**: Includes a webhook service for handling WhatsApp interactions.
- **AI-Ready**: Structured to support AI-driven customer service features.

## 🛠️ Tech Stack

### Backend

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.x
- **Database ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Validation**: Pydantic

### Frontend

- **Core**: HTML5, CSS3, Vanilla JavaScript

## 📂 Project Structure

```text
├── backend/
│   ├── api/            # API endpoints (appointments, chat, etc.)
│   ├── core/           # Configuration and database connections
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic data schemas
│   ├── services/       # Business logic (Booking, WhatsApp)
│   └── main.py         # Application entry point
└── frontend/
    └── index.html      # Main user interface
```
