# Tasks: Import Error Fix - Database Dependencies

**Feature Branch**: `001-phase-2-docker`
**Input**: Import error report - 'app.database' se 'get_db' import nahi ho raha
**Prerequisites**: Phase 1-7 complete, backend structure established

**Tests**: Manual testing - ensure application starts without import errors

**Organization**: Fix-focused tasks with clear file paths

---

## Context

**Import Error**: Multiple routers import `get_db` from `app.database`, but database.py exports `get_session` instead.

**Additional Issue**: `models.py` imports `Base` from `.database`, but SQLModel-based database.py doesn't expose `Base`.

**Goal**: Fix imports so that:
1. `get_db()` function available for dependency injection
2. `Base` class available for model inheritance
3. Application starts without errors: `uvicorn app.main:app`

---

## Phase 1: Database Module Fixes (Priority: P0) 🎯 CRITICAL

**Goal**: `app/database.py` mein `get_db` function aur `Base` class export karna

**Independent Test**: Import statement work kare: `from app.database import get_db, Base`

### Fix Database Exports

- [X] T001 [P] Fix `backend/app/database.py` to export `get_db` function (alias ya rename `get_session` to `get_db`, ya phir `get_db = get_session` add karo)
- [X] T002 [P] Fix `backend/app/database.py` to export `Base` class (SQLModel import karo aur `Base = SQLModel.metadata` ya alag se `declarative_base()` create karo)
- [X] T003 Verify `backend/app/database.py` exports: `engine`, `create_db_and_tables`, `get_db`, `Base`, `Session`

---

## Phase 2: Router Import Verification (Priority: P0) 🎯 CRITICAL

**Goal**: Saare routers mein correct imports verify karna

**Independent Test**: Har router import ho bina error ke

### Fix Router Imports

- [ ] T004 [P] Verify `backend/app/routers/auth.py` - `from ..database import get_db` kaam kare
- [ ] T005 [P] Verify `backend/app/routers/todos.py` - `from ..database import get_db` kaam kare
- [ ] T006 [P] Verify `backend/app/routers/categories.py` - `from app.database import get_db` kaam kare
- [ ] T007 [P] Verify `backend/app/routers/analytics.py` - `from app.database import get_db` kaam kare
- [ ] T008 [P] Verify `backend/app/routers/users.py` - `from ..database import get_db` kaam kare
- [ ] T009 Verify `backend/app/auth.py` - `from .database import get_db` kaam kare
- [ ] T010 Verify `backend/app/websocket.py` - `from app.database import get_db` kaam kare (dynamic import)

---

## Phase 3: Models Import Fix (Priority: P0) 🎯 CRITICAL

**Goal**: `models.py` mein `Base` import fix karna

**Independent Test**: `models.py` import ho bina error ke

### Fix Models Import

- [ ] T011 [P] Fix `backend/app/models.py` - `from .database import Base` ko ensure karo ke kaam kare (SQLModel se `Base = SQLModel` import karo ya `declarative_base()` use karo)
- [ ] T012 Verify `backend/app/models.py` imports successfully with all model classes (User, Category, Analytics, Todo)

---

## Phase 4: Application Startup Test (Priority: P0) 🎯 CRITICAL

**Goal**: Pura application bina import error ke start ho

**Independent Test**: `uvicorn app.main:app --host 0.0.0.0 --port 8000` successfully run ho

### Test Application Startup

- [ ] T013 [P] Test: `cd backend && py -3.12 -c "from app.database import get_db, Base"` - No import errors
- [ ] T014 [P] Test: `cd backend && py -3.12 -c "from app.models import User, Category, Analytics, Todo"` - All models import
- [ ] T015 [P] Test: `cd backend && py -3.12 -c "from app.main import app"` - Main app imports
- [ ] T016 Run: `cd backend && py -3.12 -m uvicorn app.main:app --host 0.0.0.0 --port 8000` - Server starts successfully
- [ ] T017 Verify: http://localhost:8000/health - Health endpoint respond kare
- [ ] T018 Verify: http://localhost:8000/docs - Swagger UI load ho

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Description | Depends On | Blocks |
|-------|-------------|------------|--------|
| Phase 1 | Database Module Fixes | None | All (critical path) |
| Phase 2 | Router Import Verification | Phase 1 | None |
| Phase 3 | Models Import Fix | Phase 1 | None |
| Phase 4 | Application Startup Test | Phase 1, 2, 3 | None |

### Execution Order

1. **T001-T003** (Phase 1) - Database exports fix - **MUST COMPLETE FIRST**
2. **T004-T010** (Phase 2) - Router imports verify - Can run after T001
3. **T011-T012** (Phase 3) - Models import fix - Can run after T002
4. **T013-T018** (Phase 4) - Startup test - **MUST COMPLETE LAST**

---

## Parallel Opportunities

**Can run in parallel (after Phase 1)**:

```bash
# Router imports verification (different files)
Task: "T004 [P] Verify auth.py imports"
Task: "T005 [P] Verify todos.py imports"
Task: "T006 [P] Verify categories.py imports"
Task: "T007 [P] Verify analytics.py imports"
Task: "T008 [P] Verify users.py imports"
```

**Can run in parallel (startup tests)**:

```bash
# Import tests (independent)
Task: "T013 [P] Test database imports"
Task: "T014 [P] Test models imports"
Task: "T015 [P] Test main app import"
```

---

## Implementation Strategy

### MVP (Minimum Viable Fix)

1. **T001**: Add `get_db = get_session` alias in database.py
2. **T002**: Add `Base = SQLModel` or create `Base = declarative_base()` in database.py
3. **T013**: Test imports work
4. **T016**: Test server starts

**MVP Scope**: Just fix exports, verify app starts

### Complete Fix

1. Complete MVP
2. Verify all router imports (T004-T010)
3. Verify models import (T011-T012)
4. Test all endpoints (T017-T018)

---

## Technical Details

### Current Issue

**database.py exports**:
```python
engine
create_db_and_tables()
get_session()  # ← Problem: routers expect 'get_db'
# Missing: Base class
```

**Routers expect**:
```python
from app.database import get_db  # ← Error: 'get_db' not found
```

**models.py expects**:
```python
from .database import Base  # ← Error: 'Base' not found
```

### Solution Options

**Option 1: Add aliases (Recommended)**
```python
# In database.py
def get_db() -> Generator[Session, None, None]:
    """Alias for get_session for backward compatibility"""
    yield from get_session()

Base = SQLModel  # Use SQLModel as Base for models
```

**Option 2: Rename function**
```python
# Rename get_session to get_db
def get_db() -> Generator[Session, None, None]:
    ...
```

**Option 3: Create separate Base**
```python
# In database.py
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

---

## Success Criteria

| Criterion | Target | Test |
|-----------|--------|------|
| get_db export | Available | `from app.database import get_db` |
| Base export | Available | `from app.database import Base` |
| Models import | No errors | `from app.models import User` |
| Server starts | No errors | `uvicorn app.main:app` |
| Health endpoint | 200 OK | GET /health |
| Swagger UI | Loads | GET /docs |

**Overall**: 6/6 must pass

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **Priority P0** = Critical block, application nahi chal sakta without fix
- **File Path Reference**: All paths absolute from `E:\Python Codes\HackAthon 2\Phase II\`
- **Format Validation**: ✅ ALL tasks follow the checklist format

---

## Expected Outcome

After completing these tasks:

1. ✅ `from app.database import get_db` works
2. ✅ `from app.database import Base` works
3. ✅ All routers import successfully
4. ✅ Models import successfully
5. ✅ Application starts: `uvicorn app.main:app`
6. ✅ All endpoints accessible

**Estimated Time**: 15-30 minutes
**Complexity**: Low (simple exports fix)
**Risk**: Low (backward compatible changes)

---

**Ready for Implementation**: Import error fix tasks defined. Start with T001-T003 (Database Module Fixes) for MVP.
