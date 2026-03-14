# JWT Authentication and Tasks API

Complete backend API with user authentication and task management.

## Quick Start

### 1. Update Database URL

Edit `.env` file and set your Neon PostgreSQL connection string:

```env
DATABASE_URL=postgresql+psycopg://user:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### 2. Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update `.env` with the generated key:

```env
SECRET_KEY=your-generated-secret-key-here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python database/init_db.py
```

### 5. Start Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test API

Open browser to: http://localhost:8000/docs

## API Endpoints

### Authentication

- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token

### Tasks (requires authentication)

- `GET /tasks` - List all your tasks
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get specific task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

## Example Usage

### Register

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create Task

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "My First Task",
    "description": "Testing the API",
    "status": "todo"
  }'
```

### List Tasks

```bash
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (!@#$%^&*(),.?":{}|<>)

## Task Statuses

- `todo` - Task not started
- `in_progress` - Currently working on it
- `done` - Task completed

## CORS

Configured for `http://localhost:3000` (Next.js frontend).

Update in `.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Tech Stack

- **Framework**: FastAPI
- **Database ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL (Neon)
- **Authentication**: JWT with HS256
- **Password Hashing**: bcrypt
- **Validation**: Pydantic v2

## Project Structure

```
app/
├── main.py              # FastAPI application
├── config.py            # Environment configuration
├── database.py          # Database connection
├── core/
│   ├── security.py      # Password hashing, JWT
│   └── exceptions.py    # Error handling
├── models/
│   ├── user.py          # User model
│   └── task.py          # Task model
├── schemas/
│   ├── user.py          # User schemas
│   ├── token.py         # Token schemas
│   └── task.py          # Task schemas
└── api/
    ├── deps.py          # Dependencies (auth)
    ├── auth.py          # Auth endpoints
    └── tasks.py         # Task endpoints
```

## Security Notes

- JWT tokens expire after 24 hours (1440 minutes)
- Passwords are hashed with bcrypt before storage
- Users can only access their own tasks (enforced at API level)
- CORS configured for specific origins only

## Next Steps

1. ✅ Backend API complete
2. ⏳ Connect Next.js frontend to http://localhost:8000
3. ⏳ Use JWT token from login for authenticated requests
4. ⏳ Handle token expiration in frontend
