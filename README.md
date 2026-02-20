# Modern Inventory Management System

A robust, full-featured Inventory Management System built with Flask, SQLAlchemy, and Bootstrap 5.

## Features

- **User Authentication**: Secure login and registration system.
- **Modern Dashboard**: Real-time statistics on products, stock levels, and value.
- **Product Management**: Add, Edit, and Delete products with ease.
- **Low Stock Alerts**: Visual indicators for products running low on stock.
- **Review Transactions**: Log of stock changes (coming soon).
- **Export Data**: One-click CSV export of your inventory.
- **Responsive Design**: Works on desktop and mobile.

## Technology Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite (Production-ready for PostgreSQL/MySQL)
- **Containerization**: Docker & Docker Compose

## Quick Start

### Local Installation

1.  **Clone the repository** (if not already done).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    python run.py
    ```
4.  Open your browser at `http://localhost:5000`.

### Docker Installation

1.  Build and run with creating the container:
    ```bash
    docker-compose up --build
    ```
2.  Access the app at `http://localhost:5000`.

## Default Login

- **Username**: `admin`
- **Password**: `password`

## Project Structure

- `app/`: Main application package.
    - `models.py`: Database models.
    - `routes/`: Application routes (Auth, Main, Inventory).
    - `templates/`: HTML templates.
    - `static/`: CSS and JS files.
- `config.py`: Configuration settings.
- `run.py`: Application entry point.
