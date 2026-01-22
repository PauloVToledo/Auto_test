# Automotora Management System

This project is a full-stack web application for a car dealership. It features a vehicle catalog, an appointment booking system with WhatsApp notifications, and an AI-powered chatbot for customer inquiries. The entire application is containerized using Docker for easy setup and deployment.

## 🚀 Features

-   **Vehicle Catalog**: Browse, view, and filter available vehicles by brand, year, and price.
-   **Appointment Booking**: Customers can easily schedule appointments to see specific vehicles.
-   **AI Chatbot**: An integrated chatbot, powered by Google's Gemini API, answers customer questions in real-time.
-   **WhatsApp Integration**: Capable of sending booking confirmations via WhatsApp (requires Twilio configuration).
-   **RESTful API**: A well-documented FastAPI backend provides data to the frontend.
-   **Containerized**: Uses Docker and Docker Compose for a consistent development and production environment.

## 🛠️ Tech Stack

-   **Backend**:
    -   **Framework**: FastAPI
    -   **Language**: Python 3.11
    -   **Database**: PostgreSQL
    -   **ORM**: SQLAlchemy with Alembic for migrations
    -   **Validation**: Pydantic
-   **Frontend**:
    -   HTML5, CSS3, Vanilla JavaScript
    -   Bootstrap 5 for styling
-   **DevOps**:
    -   Docker & Docker Compose

## 🏁 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   [Git](https://git-scm.com/)
-   A Google [Gemini API Key](https://ai.google.dev/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Create an environment file:**
    The backend service requires API keys and other secrets. Create a `.env` file in the root of the project directory.

    ```env
    # Gemini API Key for the AI Chatbot
    GEMINI_API_KEY=your_gemini_api_key_here

    # You can add other optional keys here if you extend the functionality
    # TWILIO_ACCOUNT_SID=your_twilio_sid
    # TWILIO_AUTH_TOKEN=your_twilio_token
    # GOOGLE_API_KEY=your_google_api_key
    ```
    Replace `your_gemini_api_key_here` with your actual Gemini API key.

3.  **Build and run the containers:**
    Use Docker Compose to build the images and start the services.

    ```bash
    docker-compose up -d --build
    ```

    -   The `-d` flag runs the containers in detached mode.
    -   The `--build` flag forces a rebuild of the images if the Dockerfiles have changed.

### Usage

Once the containers are running, you can access the different parts of the application:

-   **Frontend Application**: Open your browser and navigate to `http://localhost:3000`
-   **Backend API Docs**: The FastAPI backend provides automatic interactive documentation. Access it at `http://localhost:8000/docs`

## 📂 Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/            # API endpoints (appointments, chat, vehicles)
│   │   ├── core/           # Configuration, database connection
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Pydantic data schemas
│   │   ├── services/       # Business logic (AI, Booking, WhatsApp)
│   │   └── main.py         # FastAPI application entry point
│   ├── Dockerfile          # Backend Docker image instructions
│   └── tests/              # Pytest tests
├── frontend/
│   ├── app.js              # Frontend logic (fetching data, filtering, chat)
│   ├── index.html          # Main user interface
│   ├── style.css           # Custom styles
│   └── Dockerfile          # Frontend Docker image instructions (using Nginx)
├── .gitignore
├── docker-compose.yml      # Defines and orchestrates all services (db, backend, frontend)
└── README.md               # This file
```