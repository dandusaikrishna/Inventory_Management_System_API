# Inventory Management System

## Overview
A Django REST API for managing warehouse inventory with features for product and stock management.

---
## 🎥 Video Tutorials

| Tutorial | Link | Description |
|----------|------|-------------|
| 🚀 **Setup & Development** | [Watch Now](https://drive.google.com/file/d/1X-F6I-dzmwjxqGVh5LSDqdaRH1n5iD_6/view?usp=sharing) | Initial setup, configuration & API testing |


## Features
- Product Management (CRUD operations)
- Stock Movement Tracking
- Low Stock Alerts
- Comprehensive API Documentation
- Automated Tests

## Technology Stack
- Python 3.11
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose

## Project Structure
```
inventory_management/
├── inventory_management/       # Django project settings
│   ├── settings.py           # Main settings file
│   ├── urls.py               # Project URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── inventory/                # Main inventory app
│   ├── models.py             # Database models
│   ├── serializers.py        # DRF serializers
│   ├── views.py              # API views
│   ├── services.py           # Business logic services
│   ├── urls.py               # App URL configuration
│   ├── admin.py              # Django admin configuration
│   ├── helpers/              # Helper modules
│   │   ├── exceptions.py     # Custom exceptions
│   │   ├── responses.py      # Response utilities
│   │   ├── stock_helpers.py  # Stock-related helpers
│   │   └── validators.py     # Validation helpers
│   ├── migrations/           # Database migrations
│   └── tests/                # Unit and integration tests
├── Dockerfile                # Docker image configuration
├── docker-compose.yml        # Docker Compose setup
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
└── README.md                 # This file
```

## Setup and Installation

### Prerequisites
- Docker and Docker Compose (recommended)
- Python 3.11+ (for local development without Docker)
- PostgreSQL (if running locally without Docker)

### Local Development with Docker (Recommended)
1. Clone the repository
```bash
git clone <repository-url>
cd inventory_management
```

2. Create environment file
```bash
cp .env.example .env
```
Edit `.env` with your database credentials if needed (defaults are provided).

3. Start the services using Docker Compose
```bash
docker-compose up -d
```
This will start the Django application on `http://localhost:8000` and PostgreSQL database.

4. Run database migrations
```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser (optional, for Django admin access)
```bash
docker-compose exec web python manage.py createsuperuser
```

### Local Development without Docker
1. Clone the repository
```bash
git clone <repository-url>
cd inventory_management
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database and update `.env` file with database credentials.

5. Run database migrations
```bash
python manage.py migrate
```

6. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## Running Tests
To run the test suite:
```bash
# With Docker
docker-compose exec web python manage.py test

# Without Docker (in activated virtual environment)
python manage.py test
```

## API Endpoints

### Products
- `GET /api/v1/products/` - List all products
- `POST /api/v1/products/` - Create a new product
- `GET /api/v1/products/{id}/` - Get product details
- `PUT /api/v1/products/{id}/` - Update product
- `DELETE /api/v1/products/{id}/` - Delete product

### Stock Management
- `POST /api/v1/products/{id}/increase-stock/` - Increase stock
- `POST /api/v1/products/{id}/decrease-stock/` - Decrease stock
- `GET /api/v1/products/low-stock/` - List low stock products

## Assumptions and Design Choices
- **Framework Choice**: Django REST Framework (DRF) was chosen for its robust API development capabilities, serialization, and built-in features like pagination and filtering.
- **Database**: PostgreSQL is used as the primary database for its reliability and advanced features, suitable for production environments.
- **Containerization**: Docker is used for consistent development and deployment environments, making it easy to set up and run the application across different systems.
- **Architecture**: The application follows a service-oriented architecture with business logic separated into `services.py`, and helper functions organized in the `helpers/` directory for better maintainability.
- **Authentication**: No authentication is implemented by default, assuming the API will be used in a controlled environment or with external authentication mechanisms.
- **Environment Configuration**: `python-decouple` is used for managing environment variables, allowing different configurations for development, testing, and production.
- **Testing**: Django's built-in test framework is used for unit and integration tests, ensuring code reliability and preventing regressions.
- **API Versioning**: The API is versioned (v1) to allow for future changes without breaking existing clients.

## Contributing
1. Create a new branch for your feature or bug fix
2. Make your changes
3. Write or update tests as necessary
4. Run the test suite to ensure everything works
5. Submit a pull request with a clear description of the changes

