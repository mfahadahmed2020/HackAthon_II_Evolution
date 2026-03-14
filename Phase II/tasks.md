# Tasks: Evolution of Todo - Phase II (Multi-User Web App with Authentication)

**Input**: Design documents from `/specs/`
- plan.md: Technology stack, project structure, 7-phase implementation plan
- specs/ui/components.md: 14 reusable UI components
- specs/ui/pages.md: Page layouts and user flows
- specs/features/authentication-ui.md: Auth UI with JWT management
- specs/features/task-ui.md: Task CRUD UI specifications

**Tests**: Tests are OPTIONAL for this feature - implementation first, testing in Phase 6 per project plan

**Organization**: Tasks organized by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo**: `backend/` and `frontend/` at repository root
- **Backend**: Python FastAPI in `backend/app/`
- **Frontend**: Next.js 16+ in `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment configuration

- [ ] T001 Verify monorepo structure: `backend/`, `frontend/`, `specs/` directories exist
- [ ] T002 Create root `.env` file with BETTER_AUTH_SECRET, DATABASE_URL, BACKEND_URL
- [ ] T003 [P] Create `frontend/.env.local` with NEXT_PUBLIC_API_URL
- [ ] T004 [P] Install frontend dependencies: `cd frontend && npm install`
- [ ] T005 [P] Install backend dependencies: `cd backend && pip install -r requirements.txt`
- [ ] T006 [P] Create 7 agent files in `.qwen/agents/` directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Generate BETTER_AUTH_SECRET using openssl rand -base64 32
- [ ] T008 Setup Neon PostgreSQL connection in `backend/database/connection.py`
- [ ] T009 [P] Create User SQLModel in `backend/app/models/user.py`
- [ ] T010 [P] Create Task SQLModel in `backend/app/models/task.py`
- [ ] T011 Create database initialization script in `backend/database/init_db.py`
- [ ] T012 [P] Setup FastAPI CORS middleware in `backend/main.py`
- [ ] T013 [P] Implement JWT token generation utility in `backend/utils/jwt.py`
- [ ] T014 [P] Implement JWT verification dependency in `backend/middleware/auth.py`
- [ ] T015 Create base API router structure in `backend/api/router.py`
- [ ] T016 [P] Setup frontend API client in `frontend/lib/api.ts`
- [ ] T017 [P] Create AuthContext in `frontend/contexts/auth-context.tsx`
- [ ] T018 [P] Implement theme provider in `frontend/components/theme-provider.tsx`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can signup, login, and access protected dashboard with JWT authentication

**Independent Test**: User can create account, login, and access `/dashboard` (redirects if not authenticated)

### Implementation for User Story 1

- [ ] T019 [P] [US1] Create signup request/response Pydantic models in `backend/api/schemas/auth.py`
- [ ] T020 [P] [US1] Implement password hashing utility in `backend/utils/password.py`
- [ ] T021 [US1] Implement POST `/api/auth/signup` endpoint in `backend/api/routes/auth.py`
- [ ] T022 [P] [US1] Create login request/response Pydantic models in `backend/api/schemas/auth.py`
- [ ] T023 [US1] Implement POST `/api/auth/login` endpoint in `backend/api/routes/auth.py`
- [ ] T024 [P] [US1] Create signup page component in `frontend/app/(auth)/signup/page.tsx`
- [ ] T025 [P] [US1] Create login page component in `frontend/app/(auth)/login/page.tsx`
- [ ] T026 [US1] Implement form validation for signup in `frontend/app/(auth)/signup/page.tsx`
- [ ] T027 [US1] Implement form validation for login in `frontend/app/(auth)/login/page.tsx`
- [ ] T028 [US1] Add JWT storage to localStorage in `frontend/contexts/auth-context.tsx`
- [ ] T029 [US1] Implement protected route middleware in `frontend/middleware.ts`
- [ ] T030 [US1] Add auto-redirect to dashboard after successful login
- [ ] T031 [US1] Add toast notifications for auth success/error in `frontend/app/(auth)/login/page.tsx`
- [ ] T032 [US1] Implement logout functionality in `frontend/contexts/auth-context.tsx`

**Checkpoint**: User Story 1 complete - users can signup, login, logout, and access protected routes

---

## Phase 4: User Story 2 - Task CRUD Operations (Priority: P1) 🎯 MVP

**Goal**: Users can create, read, update, and delete tasks with full user ownership enforcement

**Independent Test**: Logged-in user can create task, view only their tasks, edit, delete with user isolation verified

### Implementation for User Story 2

- [ ] T033 [P] [US2] Create task request/response Pydantic models in `backend/api/schemas/task.py`
- [ ] T034 [P] [US2] Implement task repository with user_id filtering in `backend/repositories/task_repository.py`
- [ ] T035 [US2] Implement GET `/api/tasks` endpoint with user filtering in `backend/api/routes/tasks.py`
- [ ] T036 [US2] Implement POST `/api/tasks` endpoint with user_id from JWT in `backend/api/routes/tasks.py`
- [ ] T037 [US2] Implement PUT `/api/tasks/:id` endpoint with ownership check in `backend/api/routes/tasks.py`
- [ ] T038 [US2] Implement DELETE `/api/tasks/:id` endpoint with ownership check in `backend/api/routes/tasks.py`
- [ ] T039 [P] [US2] Create TaskCard component in `frontend/components/tasks/task-card.tsx`
- [ ] T040 [P] [US2] Create TaskModal component for add/edit in `frontend/components/tasks/task-modal.tsx`
- [ ] T041 [P] [US2] Create TaskList component in `frontend/components/tasks/task-list.tsx`
- [ ] T042 [P] [US2] Create EmptyState component in `frontend/components/tasks/empty-state.tsx`
- [ ] T043 [P] [US2] Create loading skeleton in `frontend/components/tasks/task-list-skeleton.tsx`
- [ ] T044 [US2] Implement dashboard main page in `frontend/app/dashboard/page.tsx`
- [ ] T045 [US2] Implement page header with "Add New Task" button in `frontend/components/tasks/page-header.tsx`
- [ ] T046 [US2] Implement filter and sort bar in `frontend/components/tasks/filter-sort-bar.tsx`
- [ ] T047 [US2] Add optimistic update for task creation in `frontend/app/dashboard/page.tsx`
- [ ] T048 [US2] Add optimistic update for task toggle complete in `frontend/app/dashboard/page.tsx`
- [ ] T049 [US2] Implement delete confirmation modal in `frontend/components/tasks/delete-confirmation-modal.tsx`
- [ ] T050 [US2] Add toast notifications for CRUD operations in `frontend/app/dashboard/page.tsx`
- [ ] T051 [US2] Implement task edit functionality via modal in `frontend/components/tasks/task-card.tsx`
- [ ] T052 [US2] Add priority badge colors (low/medium/high) in `frontend/components/tasks/task-card.tsx`
- [ ] T053 [US2] Implement relative date formatting for created date in `frontend/components/tasks/task-card.tsx`
- [ ] T054 [US2] Add strike-through and fade effect for completed tasks in `frontend/components/tasks/task-card.tsx`

**Checkpoint**: User Story 2 complete - full task CRUD with user isolation working

---

## Phase 5: User Story 3 - Dashboard Layout & Navigation (Priority: P2)

**Goal**: Professional dashboard with sidebar navigation, top nav, and responsive layout

**Independent Test**: Dashboard displays with sidebar (collapsible on mobile), top nav with theme toggle and user avatar

### Implementation for User Story 3

- [ ] T055 [P] [US3] Create Sidebar component in `frontend/components/dashboard/sidebar.tsx`
- [ ] T056 [P] [US3] Create TopNav component in `frontend/components/dashboard/top-nav.tsx`
- [ ] T057 [P] [US3] Create Avatar component in `frontend/components/ui/avatar.tsx`
- [ ] T058 [P] [US3] Create ThemeToggle component in `frontend/components/ui/theme-toggle.tsx`
- [ ] T059 [P] [US3] Create DropdownMenu for user menu in `frontend/components/ui/dropdown-menu.tsx`
- [ ] T060 [US3] Implement dashboard layout in `frontend/app/dashboard/layout.tsx`
- [ ] T061 [US3] Add mobile-responsive sidebar with hamburger menu in `frontend/components/dashboard/sidebar.tsx`
- [ ] T062 [US3] Implement navigation items (All Tasks, Pending, Completed, Profile) in `frontend/components/dashboard/sidebar.tsx`
- [ ] T063 [US3] Add user avatar dropdown with logout in `frontend/components/dashboard/top-nav.tsx`
- [ ] T064 [US3] Implement dark mode persistence in localStorage in `frontend/components/theme-provider.tsx`
- [ ] T065 [US3] Add system preference detection for theme in `frontend/components/theme-provider.tsx`
- [ ] T066 [US3] Style sidebar with active state highlighting in `frontend/components/dashboard/sidebar.tsx`
- [ ] T067 [US3] Add smooth transitions for theme switching in `frontend/app/layout.tsx`

**Checkpoint**: User Story 3 complete - professional dashboard with full navigation working

---

## Phase 6: User Story 4 - Task Filtering & Sorting (Priority: P2)

**Goal**: Users can filter tasks by status and sort by multiple criteria

**Independent Test**: Filter tabs and sort dropdown work correctly, URL updates with state, state persists on refresh

### Implementation for User Story 4

- [ ] T068 [P] [US4] Create Tabs component in `frontend/components/ui/tabs.tsx`
- [ ] T069 [P] [US4] Create Select component in `frontend/components/ui/select.tsx`
- [ ] T070 [US4] Implement filter state management in `frontend/app/dashboard/page.tsx`
- [ ] T071 [US4] Implement sort state management in `frontend/app/dashboard/page.tsx`
- [ ] T072 [US4] Add URL query param sync for filter/sort in `frontend/app/dashboard/page.tsx`
- [ ] T073 [US4] Implement pending tasks filtered view in `frontend/app/dashboard/pending/page.tsx`
- [ ] T074 [US4] Implement completed tasks filtered view in `frontend/app/dashboard/completed/page.tsx`
- [ ] T075 [US4] Add backend support for status filter in GET `/api/tasks` in `backend/api/routes/tasks.py`
- [ ] T076 [US4] Add backend support for sorting in GET `/api/tasks` in `backend/api/routes/tasks.py`
- [ ] T077 [US4] Implement filter persistence across page refresh in `frontend/app/dashboard/page.tsx`

**Checkpoint**: User Story 4 complete - filtering and sorting fully functional

---

## Phase 7: User Story 5 - Profile & Account Management (Priority: P3)

**Goal**: Users can view and manage their profile settings

**Independent Test**: Profile page displays user info, theme toggle works, account deletion option available

### Implementation for User Story 5

- [ ] T078 [P] [US5] Create Badge component in `frontend/components/ui/badge.tsx`
- [ ] T079 [P] [US5] Create Skeleton component in `frontend/components/ui/skeleton.tsx`
- [ ] T080 [P] [US5] Create Toast component in `frontend/components/ui/toast.tsx`
- [ ] T081 [US5] Implement profile page in `frontend/app/dashboard/profile/page.tsx`
- [ ] T082 [US5] Add account information card (read-only name/email) in `frontend/app/dashboard/profile/page.tsx`
- [ ] T083 [US5] Add preferences card with theme toggle in `frontend/app/dashboard/profile/page.tsx`
- [ ] T084 [US5] Add danger zone card with delete account option in `frontend/app/dashboard/profile/page.tsx`
- [ ] T085 [US5] Implement GET `/api/auth/me` endpoint in `backend/api/routes/auth.py`
- [ ] T086 [US5] Implement DELETE `/api/auth/account` endpoint in `backend/api/routes/auth.py`
- [ ] T087 [US5] Add confirmation modal for account deletion in `frontend/app/dashboard/profile/page.tsx`

**Checkpoint**: User Story 5 complete - profile management fully functional

---

## Phase 8: User Story 6 - Enhanced Task Features (Priority: P3)

**Goal**: Tasks support due dates, priority selection, and enhanced metadata

**Independent Test**: Task modal includes due date picker, priority selector, all fields persist correctly

### Implementation for User Story 6

- [ ] T088 [P] [US6] Create Input component with date type in `frontend/components/ui/input.tsx`
- [ ] T089 [P] [US6] Create Textarea component in `frontend/components/ui/textarea.tsx`
- [ ] T090 [P] [US6] Create Checkbox component in `frontend/components/ui/checkbox.tsx`
- [ ] T091 [P] [US6] Create Dialog component in `frontend/components/ui/dialog.tsx`
- [ ] T092 [US6] Update task modal with due date picker in `frontend/components/tasks/task-modal.tsx`
- [ ] T093 [US6] Add past date validation in `frontend/components/tasks/task-modal.tsx`
- [ ] T094 [US6] Add character counter for description in `frontend/components/tasks/task-modal.tsx`
- [ ] T095 [US6] Display due date on task cards in `frontend/components/tasks/task-card.tsx`
- [ ] T096 [US6] Add backend validation for due date in `backend/api/schemas/task.py`
- [ ] T097 [US6] Implement task sorting by due date in `backend/api/routes/tasks.py`

**Checkpoint**: User Story 6 complete - enhanced task features fully functional

---

## Phase 9: User Story 7 - Animations & Micro-interactions (Priority: P3)

**Goal**: Smooth animations for task add/edit/delete and state transitions

**Independent Test**: Tasks animate in/out, completion has strike-through + fade, hover effects smooth

### Implementation for User Story 7

- [ ] T098 [P] [US7] Install Framer Motion: `cd frontend && npm install framer-motion`
- [ ] T099 [P] [US7] Create animation utilities in `frontend/lib/animations.ts`
- [ ] T100 [US7] Add enter animation for new tasks in `frontend/components/tasks/task-list.tsx`
- [ ] T101 [US7] Add exit animation for deleted tasks in `frontend/components/tasks/task-list.tsx`
- [ ] T102 [US7] Add layout animation for filter/sort changes in `frontend/components/tasks/task-list.tsx`
- [ ] T103 [US7] Add hover lift effect to task cards in `frontend/components/tasks/task-card.tsx`
- [ ] T104 [US7] Add smooth transition for completion strike-through in `frontend/components/tasks/task-card.tsx`
- [ ] T105 [US7] Add modal open/close animations in `frontend/components/tasks/task-modal.tsx`
- [ ] T106 [US7] Add toast notification animations in `frontend/components/ui/toast.tsx`

**Checkpoint**: User Story 7 complete - all animations smooth and polished

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T107 [P] Add comprehensive error boundaries in `frontend/components/error-boundary.tsx`
- [ ] T108 [P] Add 404 page in `frontend/app/not-found.tsx`
- [ ] T109 [P] Add loading page in `frontend/app/loading.tsx`
- [ ] T110 [P] Add robots.txt in `frontend/public/robots.txt`
- [ ] T111 [P] Add favicon in `frontend/app/favicon.ico`
- [ ] T112 Update README.md with setup instructions and screenshots
- [ ] T113 Code cleanup and remove unused imports across all files
- [ ] T114 Performance optimization: lazy load components in `frontend/components/`
- [ ] T115 Security hardening: validate all inputs, sanitize outputs
- [ ] T116 [P] Add OpenAPI documentation in `backend/main.py`
- [ ] T117 [P] Create deployment configuration for Vercel (frontend)
- [ ] T118 [P] Create deployment configuration for Railway/Render (backend)
- [ ] T119 Test full user journey end-to-end manually
- [ ] T120 Create demo video script and record walkthrough

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Auth - Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Task CRUD - Can start after Foundational + US1 (for protected routes) - Independently testable
- **User Story 3 (P2)**: Dashboard Layout - Can start after US2 (needs task components) - Independently testable
- **User Story 4 (P2)**: Filtering - Can start after US2 + US3 - Independently testable
- **User Story 5 (P3)**: Profile - Can start after US1 (needs auth) - Independently testable
- **User Story 6 (P3)**: Enhanced Tasks - Can start after US2 - Independently testable
- **User Story 7 (P3)**: Animations - Can start after US2 - Independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Backend endpoints before frontend integration
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**:
- T003, T004, T005, T006 can all run in parallel

**Phase 2 (Foundational)**:
- T009, T010, T012, T013, T014, T016, T017, T018 can all run in parallel

**Phase 3 (US1 - Auth)**:
- T019, T020, T022, T024, T025 can run in parallel
- T021 depends on T019, T020
- T023 depends on T022, T020
- T026, T027 can run in parallel after T024, T025

**Phase 4 (US2 - Task CRUD)**:
- T033, T034, T039, T040, T041, T042, T043 can all run in parallel
- T035, T036, T037, T038 depend on T033, T034
- T044 depends on T039-T043
- T045-T054 can run in parallel after T044

**Phase 5 (US3 - Dashboard)**:
- T055, T056, T057, T058, T059 can run in parallel
- T060 depends on T055, T056
- T061-T067 can run in parallel after T060

**Phase 6+**: Similar parallel patterns within each story

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch all parallel tasks for User Story 1:

# Backend schemas (T019, T022):
Task: "Create signup request/response Pydantic models in backend/api/schemas/auth.py"
Task: "Create login request/response Pydantic models in backend/api/schemas/auth.py"

# Backend utilities (T020):
Task: "Implement password hashing utility in backend/utils/password.py"

# Frontend pages (T024, T025):
Task: "Create signup page component in frontend/app/(auth)/signup/page.tsx"
Task: "Create login page component in frontend/app/(auth)/login/page.tsx"

# After these complete, implement endpoints (T021, T023) in parallel
```

---

## Parallel Example: User Story 2 (Task CRUD)

```bash
# Launch all parallel tasks for User Story 2:

# Backend models and schemas (T033, T034):
Task: "Create task request/response Pydantic models in backend/api/schemas/task.py"
Task: "Implement task repository with user_id filtering in backend/repositories/task_repository.py"

# Frontend components (T039-T043) - ALL can run in parallel:
Task: "Create TaskCard component in frontend/components/tasks/task-card.tsx"
Task: "Create TaskModal component for add/edit in frontend/components/tasks/task-modal.tsx"
Task: "Create TaskList component in frontend/components/tasks/task-list.tsx"
Task: "Create EmptyState component in frontend/components/tasks/empty-state.tsx"
Task: "Create loading skeleton in frontend/components/tasks/task-list-skeleton.tsx"

# After components complete, implement dashboard page (T044)
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T018) - **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 (T019-T032) - Auth working
4. Complete Phase 4: User Story 2 (T033-T054) - Task CRUD working
5. **STOP and VALIDATE**: Test full MVP flow (signup → login → create task → view → edit → delete)
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Auth) → Test independently → Demo ready
3. Add User Story 2 (Task CRUD) → Test independently → **MVP COMPLETE**
4. Add User Story 3 (Dashboard Layout) → Test independently → Enhanced UX
5. Add User Story 4 (Filtering) → Test independently → Better UX
6. Add User Story 5 (Profile) → Test independently → Complete app
7. Add User Story 6 (Enhanced Tasks) → Test independently → Full features
8. Add User Story 7 (Animations) → Test independently → Polished experience

### Parallel Team Strategy (7 Agents)

With 7 specialized agents working in parallel:

**Day 1-2**: All agents complete Phase 1 + Phase 2 together
- Architecture Planner: T001, T002, T008, T011, T015
- Database Engineer: T009, T010, T011
- Backend Engineer: T012, T013, T014, T015
- Frontend Engineer: T016, T017, T018
- Auth Agent: T007, T013, T014
- Spec Writer: Documentation
- Integration Tester: Setup test framework

**Day 3-4**: Parallel user story implementation
- Auth Agent + Backend Engineer: Phase 3 (US1)
- Database Engineer: Support US1 + start US2 models
- Frontend Engineer: Phase 3 (US1 UI) + Phase 4 (US2 components)
- Backend Engineer: Phase 4 (US2 endpoints)
- Integration Tester: Test US1 flow
- Spec Writer: Update docs
- Architecture Planner: Ensure consistency

**Day 5-7**: Continue parallel implementation
- All agents work on remaining user stories based on expertise
- Integration Tester: Continuous validation
- Spec Writer: Documentation + demo script

---

## Task Summary

**Total Tasks**: 120

**By Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 12 tasks
- Phase 3 (US1 - Auth): 14 tasks
- Phase 4 (US2 - Task CRUD): 22 tasks
- Phase 5 (US3 - Dashboard): 13 tasks
- Phase 6 (US4 - Filtering): 10 tasks
- Phase 7 (US5 - Profile): 10 tasks
- Phase 8 (US6 - Enhanced): 10 tasks
- Phase 9 (US7 - Animations): 9 tasks
- Phase 10 (Polish): 14 tasks

**By User Story**:
- US1 (Auth): 14 tasks
- US2 (Task CRUD): 22 tasks
- US3 (Dashboard): 13 tasks
- US4 (Filtering): 10 tasks
- US5 (Profile): 10 tasks
- US6 (Enhanced Tasks): 10 tasks
- US7 (Animations): 9 tasks
- Foundational (shared): 12 tasks
- Setup (shared): 6 tasks
- Polish (cross-cutting): 14 tasks

**Parallel Opportunities**:
- Phase 1: 4 tasks can run in parallel
- Phase 2: 8 tasks can run in parallel
- Phase 3-9: 40-60% of tasks within each story can run in parallel
- Different user stories can run in parallel after Foundational phase

**Independent Test Criteria**:
- US1: Can signup, login, access protected route
- US2: Can create/view/edit/delete tasks with user isolation
- US3: Dashboard displays with navigation working
- US4: Filter/sort changes task list correctly
- US5: Profile page shows user info, theme toggle works
- US6: Due dates and priority selection working
- US7: Animations smooth, no performance issues

**Suggested MVP Scope**: User Story 1 + User Story 2 (T001-T054)
- Complete authentication flow
- Full task CRUD with user isolation
- Basic functional UI (polish in later iterations)

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group of 2-3 tasks
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **CRITICAL**: Complete Phase 2 (Foundational) before starting ANY user story
- **Agent Workflow**: Route tasks to appropriate agents based on expertise (see plan.md)
