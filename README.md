# 📦 Order Management System using FastAPI

An Order Management API built with FastAPI to handle users, authentication, and full CRUD operations for orders.

## 🚀 Tech Stack
- Python 3.x
- FastAPI
- SQLAlchemy / ORM
- Alembic (Migrations)
- Pydantic
- SQLite / PostgreSQL / MySQL
- Uvicorn

## 📁 Project Structure
/app/
  ├── main.py
  ├── auth/
  ├── models/
  ├── schema/
  ├── crud/
  ├── api/
  ├── utils/
  
/seed/
 /alembic/
.env
requirements.txt
test.py

## ✅ Features
- User authentication (signup / login / token-based)
- CRUD operations for orders
- Modular and clean architecture
- Pydantic-based validation
- Alembic migrations
- Async FastAPI structure
- Ready for extension

## 🔧 Installation & Setup

### 1. Clone the repository
git clone https://github.com/Sameerpawar24/Order-Management-System-Using-FastAPI.git
cd Order-Management-System-Using-FastAPI

### 2. Install dependencies
pip install -r requirements.txt

### 3. Setup environment variables
Create a `.env` file:
DATABASE_URL=sqlite:///./orders.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

### 4. Run database migrations
alembic upgrade head

### 5. Start the server
uvicorn main:app --reload

### 6. Access API Docs
http://localhost:8000/docs

## 🧪 Running Tests
pytest
or:
python test.py

## 📈 Future Improvements
- Add product/item management
- Add inventory management
- Add user roles (Admin/User)
- Add pagination & filters
- Add refresh tokens
- Add Docker support

## 📄 License
Add your project license here (MIT recommended).
