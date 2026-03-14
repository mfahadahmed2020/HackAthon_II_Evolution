# Database Migration Guide: SQLite to Neon PostgreSQL

SQLite se Neon PostgreSQL par shift hone ke liye yeh steps follow karein.

## ✅ Migration Complete

Aapka backend ab Neon PostgreSQL use karne ke liye configure ho gaya hai!

## Configuration Summary

### 1. Database URL Updated ✓

**.env file mein:**
```env
DATABASE_URL=postgresql://user:password@your-neon-host/neondb?sslmode=require
```

**Important:** Apna actual Neon connection URL paste karein. Yeh format hai:
```
postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

### 2. CORS Enabled for localhost:3000 ✓

Next.js frontend ke liye CORS properly configure ho gaya hai:

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Connection Pooling ✓

Neon PostgreSQL ke liye optimized connection pooling:
- `pool_pre_ping=True` - Connection drops ko automatically handle karta hai
- `pool_size=10` - 10 concurrent connections
- `max_overflow=20` - Extra 20 connections allow

## Setup Steps

### Step 1: Install PostgreSQL Driver

```bash
pip install psycopg[binary]
```

Ya agar already install hai, toh verify karein:

```bash
pip show psycopg
```

### Step 2: Get Your Neon Connection String

1. [Neon Dashboard](https://console.neon.tech/) par jayein
2. Apna project select karein
3. "Connection Details" par click karein
4. Connection string copy karein (Psql or URI format)
5. `.env` file mein `DATABASE_URL` ko update karein

**Example:**
```env
DATABASE_URL=postgresql://john:abc123@ep-cool-darkness-123456.us-east-1.aws.neon.tech/mydb?sslmode=require
```

### Step 3: Database Tables Create Karein

```bash
python database/init_db.py
```

Yeh command Neon par yeh tables create karega:
- `users` - Authentication ke liye
- `tasks` - Task management ke liye

### Step 4: Server Start Karein

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Verify Connection

Browser mein open karein: http://localhost:8000/health

Response aana chahiye:
```json
{
  "status": "healthy",
  "app_name": "JWT Auth and Tasks API",
  "version": "1.0.0"
}
```

## Testing API

### 1. User Registration

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

### 2. User Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

Response mein `access_token` milega.

### 3. Create Task (Authenticated)

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "My First Task",
    "description": "Testing Neon PostgreSQL",
    "status": "todo"
  }'
```

### 4. List Tasks

```bash
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Frontend Integration (Next.js)

Aapka Next.js frontend ab API se connect kar sakta hai:

### Environment Variables (Next.js)

**.env.local** in Next.js project:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### API Calls

```typescript
// Login example
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
})

const { access_token } = await response.json()

// Authenticated request
const tasks = await fetch('http://localhost:8000/tasks', {
  headers: { 'Authorization': `Bearer ${access_token}` }
})
```

## Troubleshooting

### Error: "could not connect to server"

**Solution:**
1. Verify `DATABASE_URL` in `.env` is correct
2. Check Neon dashboard mein connection allowed hai
3. Internet connection check karein

### Error: "password authentication failed"

**Solution:**
1. Neon dashboard se correct password copy karein
2. Special characters ko URL encode karein (e.g., `@` → `%40`)

### Error: "psycopg module not found"

**Solution:**
```bash
pip install psycopg[binary]
```

### CORS Error from Frontend

**Solution:**
1. Verify `ALLOWED_ORIGINS=http://localhost:3000` in `.env`
2. Backend server restart karein
3. Frontend mein correct API URL use ho raha hai verify karein

## SQLite vs PostgreSQL Differences

| Feature | SQLite | PostgreSQL (Neon) |
|---------|--------|-------------------|
| Type | File-based | Server-based |
| Concurrency | Limited | High (100+ users) |
| Connection | Local file | Network (SSL) |
| Best for | Development | Production |

## Benefits of Neon PostgreSQL

✅ **Production Ready** - High availability aur scalability
✅ **Serverless** - Automatic scaling aur connection pooling
✅ **SSL Enabled** - Secure connections by default
✅ **Free Tier** - 0.5 GB storage, sufficient for starting
✅ **Branching** - Database branching for development

## Next Steps

1. ✅ Database configured for Neon PostgreSQL
2. ✅ CORS enabled for localhost:3000
3. ⏳ Connect Next.js frontend
4. ⏳ Deploy to production (optional)

## Support

Agar koi issue ho toh:
- Neon Docs: https://neon.tech/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- SQLModel Docs: https://sqlmodel.tiangolo.com
