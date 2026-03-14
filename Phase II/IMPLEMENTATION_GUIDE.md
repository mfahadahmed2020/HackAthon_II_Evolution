# 🚀 Phase 2 Implementation Guide

## Quick Start Instructions

### Step 1: Generate BETTER_AUTH_SECRET

**Visit Better Auth Docs:**
1. Go to: https://www.better-auth.com/docs/installation
2. Click **"Generate Secret"** button
3. Copy the generated key (looks like: `xJ8...kL9=`)

**OR generate via command:**
```bash
openssl rand -base64 32
```

---

### Step 2: Create Environment Files

#### Root `.env` file (`E:\Python Codes\HackAthon 2\Phase II\.env`):
```env
# Better Auth (REQUIRED - replace with your generated secret)
BETTER_AUTH_SECRET=your-generated-secret-key-here-minimum-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Database (Neon PostgreSQL) - Replace with your actual connection string
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# Backend API
BACKEND_URL=http://localhost:8000
```

#### Frontend `.env.local` file (`frontend\.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Evolution of Todo
```

---

### Step 3: Install Frontend Dependencies

**Wait for npm install to complete** (already running in background):
```bash
cd frontend
npm install
```

**If you encounter the `tw-animate-css` error:**
```bash
npm install tw-animate-css
```

Then check `tailwind.config.ts` for proper configuration.

---

### Step 4: Run Frontend Development Server

```bash
cd frontend
npm run dev
```

This should start the Next.js dev server on **http://localhost:3000**

---

### Step 5: Run Backend Server (in separate terminal)

```bash
cd backend
# Activate virtual environment if not already done
.\venv\Scripts\activate  # Windows

# Install dependencies if needed
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🐛 Troubleshooting

### Error: "Can't resolve tw-animate-css"

**Solution 1: Install missing package**
```bash
cd frontend
npm install tw-animate-css
```

**Solution 2: Check globals.css import**
Open `frontend/app/globals.css` and verify the import statement:
```css
@import "tw-animate-css";  /* Make sure this exists */
```

**Solution 3: Update tailwind.config.ts**
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
export default config
```

---

### Error: "Module not found: Can't resolve '@/..."

**Solution:** Check `tsconfig.json` has proper paths:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

---

### Error: "Authentication failed" or Database connection errors

**Check:**
1. `DATABASE_URL` in `.env` is correct
2. Network connection to Neon is working
3. SSL mode is set: `?sslmode=require`

---

### Error: "CORS Error" in browser console

**Solution:** Configure CORS in FastAPI backend:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ✅ Success Checklist

- [ ] `npm install` completed without errors
- [ ] `npm run dev` starts successfully on port 3000
- [ ] Backend server running on port 8000
- [ ] Can access http://localhost:3000 in browser
- [ ] Login/Register pages load correctly
- [ ] No console errors in browser DevTools
- [ ] API calls to backend working (check Network tab)

---

## 📋 If Errors Persist - Use These Prompts

### Prompt 1: General Startup Check
```
Hi, could you please run my Next.js project using npm run dev (or npm start if configured) 
and check if it starts correctly? If there are any errors, please try to resolve them so 
that the project runs successfully on your environment.

The project is in the frontend folder, and all TypeScript and Next.js configurations are 
already set up.
```

### Prompt 2: tw-animate-css Error (Recommended)
```
I am getting a 'Can't resolve tw-animate-css' error in my Next.js 16 project while running 
'npm run dev'. It seems like a missing dependency or a wrong import in my globals.css. 

Please provide the terminal command to install the missing package and check if there's 
any configuration needed in tailwind.config.ts.
```

### Prompt 3: CSS Compilation Error
```
My Next.js application is failing to compile with 'CssSyntaxError' because it cannot find 
'tw-animate-css'. Here is the error log:

[PASTE YOUR ERROR LOG HERE]

How do I fix this? Should I install it via npm or is it a typo in my @import statement 
in globals.css?
```

---

## 📁 Project Structure Reference

```
Phase II/
├── frontend/                 # Next.js 16+ Frontend
│   ├── app/                 # App Router pages
│   │   ├── login/          # Login page
│   │   ├── register/       # Signup page
│   │   ├── dashboard/      # Protected dashboard
│   │   └── page.tsx        # Home (redirects)
│   ├── components/          # React components
│   ├── lib/                # Utilities (api.ts, types.ts)
│   └── .env.local          # Frontend env vars
│
├── backend/                 # FastAPI Backend
│   ├── main.py             # FastAPI app
│   ├── models/             # SQLModel schemas
│   ├── api/                # API routes
│   └── .env                # Backend env vars
│
├── specs/                   # Specifications
│   ├── ui/                 # UI specs
│   ├── features/           # Feature specs
│   └── plan.md             # Project plan
│
├── .env                     # Root environment variables
└── PROJECT_CONSTITUTION.md  # Project principles
```

---

## 🎯 Next Steps After Setup

1. **Verify Frontend Runs**: Open http://localhost:3000
2. **Check Login Page**: Navigate to /login
3. **Test Backend Connection**: Check Network tab for API calls
4. **Create First Task**: Test full CRUD flow
5. **Test Dark Mode**: Toggle theme
6. **Responsive Check**: Test on mobile viewport

---

## 📞 Support Resources

- **Better Auth Docs**: https://www.better-auth.com/docs
- **Next.js 16 Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Neon PostgreSQL**: https://neon.tech/docs

---

**Generated**: 2026-03-14  
**Version**: 1.0.0  
**Status**: Ready for Implementation
