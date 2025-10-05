# Inventory Management System

## Overview
A Django REST API for managing warehouse inventory with features for product and stock management.

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
├── inventory_management/       # Project settings
│   ├── settings/
│   │   ├── base.py           # Base settings
│   │   ├── development.py    # Development settings
│   │   ├── production.py     # Production settings
│   │   └── testing.py        # Testing settings
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── inventory/            # Inventory app
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── services.py
│       └── tests/
├── scripts/                  # Utility scripts
├── requirements/             # Dependencies
└── docker/                  # Docker configurations
```

## Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- PostgreSQL

### Local Development
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

3. Copy environment file
```bash
cp .env.example .env
```

4. Start Docker services
```bash
docker-compose up -d
```

5. Run migrations
```bash
docker-compose exec web python manage.py migrate
```

6. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### Running Tests
```bash
docker-compose exec web pytest
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

## Contributing
1. Create a new branch
2. Make changes
3. Run tests
4. Submit pull request

