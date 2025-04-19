# Op Food Shop

**Op Food Shop** is a Django-based web application tailored for managing food orders, products, and users. It provides a structured backend to facilitate seamless operations for food-related businesses.

## 🚀 Features

- **User Management**: Handle user registrations, authentications, and profiles.
- **Product Management**: Add, update, and categorize food products.
- **Order Processing**: Streamlined order placement and tracking system.
- **API Integration**: Modular API structure for external integrations.

## 🛠️ Technologies Used

- **Framework**: Django
- **Language**: Python
- **Database**: PostgreSQL (or SQLite for development)
- **Others**: Django Rest Framework, Djoser, Simple JWT, 

## ⚙️ Installation

**Clone the Repository**:
   ```bash
   git clone https://github.com/Stropurbo/op-food-shop.git
   cd op-food-shop
```

**API Documentation**
```
Swagger:
http://127.0.0.1:8000/swagger/

Redoc:
http://127.0.0.1:8000/redoc/
```

**Create a Virtual Environment:**

```
    python -m venv venv
    source venv/bin/activate 
    Windows: venv\Scripts\activate
```

**Create Environment Variable**

```
create a `.env` file in the root directory and add the following steps. 

SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_URL = ***
# Optional: Cloudinary / Email / JWT settings

```

**Install Dependencies:**

```
pip install -r requirements.txt
```

**Apply Migrations:**

```
python manage.py migrate
```
**Run the Development Server:**

```
python manage.py runserver
```




