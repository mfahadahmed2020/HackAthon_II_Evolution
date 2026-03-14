/**
 * Dashboard JavaScript - Phase 7 Enhanced
 * Roman Urdu: Dashboard with categories, recurring tasks, analytics, and real-time updates
 */

let currentFilter = 'all';
let currentCategoryFilter = 'all';
let currentTodos = [];
let websocketClient = null;

// Load data on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize WebSocket for real-time updates
    initWebSocket();
    
    // Load initial data
    loadStats();
    loadAnalyticsStats();
    loadTodos();
    setupEventListeners();
    
    // Setup recurring toggle
    setupRecurringToggle();
});

function setupEventListeners() {
    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.status;
            loadTodos();
        });
    });

    // Search input with debounce
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce((e) => {
            loadTodos(e.target.value);
        }, 300));
    }

    // Todo form
    document.getElementById('todoForm').addEventListener('submit', saveTodo);
}

/**
 * Setup recurring task toggle
 * Roman Urdu: Recurring task toggle setup karna
 */
function setupRecurringToggle() {
    const recurringCheckbox = document.getElementById('todoRecurring');
    const recurrenceOptions = document.getElementById('recurrenceOptions');
    
    if (recurringCheckbox && recurrenceOptions) {
        recurringCheckbox.addEventListener('change', (e) => {
            recurrenceOptions.style.display = e.target.checked ? 'block' : 'none';
            
            // Set default start date to now
            if (e.target.checked) {
                const now = new Date();
                now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
                document.getElementById('todoStartDate').value = now.toISOString().slice(0, 16);
            }
        });
    }
}

async function loadStats() {
    try {
        const response = await apiRequest('/api/todos/stats');
        if (response) {
            const stats = await response.json();
            document.getElementById('totalTodos').textContent = stats.total;
            document.getElementById('completedTodos').textContent = stats.completed;
            document.getElementById('pendingTodos').textContent = stats.pending;
            document.getElementById('completionRate').textContent = stats.completion_percentage.toFixed(1) + '%';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadTodos(search = '') {
    try {
        let url = '/api/todos?';
        
        // Apply status filter
        if (currentFilter !== 'all') {
            url += `status_filter=${currentFilter}&`;
        }
        
        // Apply category filter (Phase 7)
        if (currentCategoryFilter && currentCategoryFilter !== 'all') {
            url += `category_id=${currentCategoryFilter}&`;
        }
        
        // Apply search
        if (search) {
            url += `search=${encodeURIComponent(search)}&`;
        }

        const response = await apiRequest(url);
        if (response) {
            const data = await response.json();
            currentTodos = data.todos;
            renderTodos(data.todos);
        }
    } catch (error) {
        console.error('Error loading todos:', error);
        showToast('Todos load nahi hue', 'error');
    }
}

/**
 * Render todos with category badges and recurrence icons (Phase 7)
 * Roman Urdu: Tasks render karna with category badges aur recurrence icons
 */
function renderTodos(todos) {
    const container = document.getElementById('todoList');

    if (todos.length === 0) {
        container.innerHTML = '<p class="empty-message">No todos found. Add one!</p>';
        return;
    }

    container.innerHTML = todos.map(todo => {
        // Get category info
        const category = todo.category_id ? getCategoryById(todo.category_id) : null;
        const categoryBadge = category 
            ? `<span class="category-badge" style="background-color: ${category.color};" title="${escapeHtml(category.name)}">${escapeHtml(category.name)}</span>`
            : '';
        
        // Recurrence icon (Phase 7)
        const recurrenceIcon = (todo.recurrence_pattern || todo.parent_id)
            ? '<span class="recurrence-icon" title="Recurring task">🔄</span>'
            : '';
        
        return `
            <div class="todo-item ${todo.status === 'completed' ? 'completed' : ''} flash-animation" data-id="${todo.id}">
                <div class="todo-info">
                    <div class="todo-title-row">
                        <div class="todo-title">${escapeHtml(todo.title)}</div>
                        ${recurrenceIcon}
                    </div>
                    ${todo.description ? `<div class="todo-description">${escapeHtml(todo.description)}</div>` : ''}
                    <div class="todo-meta">
                        <span class="priority-badge priority-${todo.priority}">${todo.priority}</span>
                        ${categoryBadge}
                        ${todo.due_date ? `<span class="due-date">📅 ${formatDate(todo.due_date)}</span>` : ''}
                    </div>
                </div>
                <div class="todo-actions">
                    ${todo.status === 'pending'
                        ? `<button class="btn-complete" onclick="markComplete(${todo.id})">✓</button>`
                        : `<button class="btn-pending" onclick="markPending(${todo.id})">↩</button>`
                    }
                    <button class="btn-edit" onclick="editTodo(${todo.id})">✎</button>
                    <button class="btn-delete" onclick="deleteTodo(${todo.id})">🗑</button>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Show add modal with reset (Phase 7)
 * Roman Urdu: Add modal show karna with reset
 */
function showAddModal() {
    document.getElementById('modalTitle').textContent = 'Add New Todo';
    document.getElementById('todoId').value = '';
    document.getElementById('todoForm').reset();
    
    // Reset recurring options
    document.getElementById('todoRecurring').checked = false;
    document.getElementById('recurrenceOptions').style.display = 'none';
    
    document.getElementById('todoModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('todoModal').style.display = 'none';
}

/**
 * Save todo with recurring support (Phase 7)
 * Roman Urdu: Todo save karna with recurring support
 */
async function saveTodo(e) {
    e.preventDefault();

    const todoId = document.getElementById('todoId').value;
    const isRecurring = document.getElementById('todoRecurring').checked;
    
    // Validate form
    const title = document.getElementById('todoTitle').value.trim();
    if (!title) {
        showToast('Title zaroori hai', 'error');
        return;
    }

    if (isRecurring) {
        // Create recurring task
        await createRecurringTask();
    } else {
        // Create/update regular todo
        const todoData = {
            title: title,
            description: document.getElementById('todoDescription').value.trim(),
            priority: document.getElementById('todoPriority').value,
            due_date: document.getElementById('todoDueDate').value || null,
            category_id: document.getElementById('todoCategory').value || null
        };

        try {
            const url = todoId ? `/api/todos/${todoId}` : '/api/todos';
            const method = todoId ? 'PUT' : 'POST';

            const response = await apiRequest(url, {
                method,
                body: JSON.stringify(todoData)
            });

            if (response && response.ok) {
                closeModal();
                loadTodos();
                loadStats();
                
                // Broadcast to other tabs
                broadcastToLocalStorage('task.created', todoData);
                
                showToast(todoId ? 'Task updated!' : 'Task created!', 'success');
            } else if (response) {
                const error = await response.json();
                showToast(error.detail || 'Task save nahi hua', 'error');
            }
        } catch (error) {
            console.error('Error saving todo:', error);
            showToast('Task save nahi hua', 'error');
        }
    }
}

/**
 * Create recurring task (Phase 7)
 * Roman Urdu: Recurring task create karna
 */
async function createRecurringTask() {
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    const priority = document.getElementById('todoPriority').value;
    const recurrencePattern = document.getElementById('recurrencePattern').value;
    const occurrences = parseInt(document.getElementById('occurrencesCount').value);
    const startDate = document.getElementById('todoStartDate').value;
    const categoryId = document.getElementById('todoCategory').value || null;

    if (!title) {
        showToast('Title zaroori hai', 'error');
        return;
    }

    if (!startDate) {
        showToast('Start date zaroori hai', 'error');
        return;
    }

    try {
        const response = await apiRequest('/api/tasks/recurring', {
            method: 'POST',
            body: JSON.stringify({
                title,
                description,
                priority,
                recurrence_pattern: recurrencePattern,
                occurrences,
                start_date: new Date(startDate).toISOString(),
                category_id: categoryId ? parseInt(categoryId) : null
            })
        });

        if (response && response.ok) {
            const result = await response.json();
            closeModal();
            loadTodos();
            loadStats();
            
            // Broadcast to other tabs
            broadcastToLocalStorage('task.created', { 
                title, 
                recurring: true, 
                count: result.created_count 
            });
            
            showToast(`${result.created_count} recurring tasks created!`, 'success');
        } else if (response) {
            const error = await response.json();
            showToast(error.detail || 'Recurring task create nahi hua', 'error');
        }
    } catch (error) {
        console.error('Error creating recurring task:', error);
        showToast('Recurring task create nahi hua', 'error');
    }
}

async function markComplete(todoId) {
    try {
        const response = await apiRequest(`/api/todos/${todoId}/complete`, { method: 'PATCH' });
        if (response && response.ok) {
            loadTodos();
            loadStats();
            
            // Broadcast to other tabs
            broadcastToLocalStorage('task.updated', { id: todoId, status: 'completed' });
        } else {
            showToast('Task complete nahi hua', 'error');
        }
    } catch (error) {
        console.error('Error marking complete:', error);
        showToast('Task complete nahi hua', 'error');
    }
}

async function markPending(todoId) {
    try {
        const response = await apiRequest(`/api/todos/${todoId}/pending`, { method: 'PATCH' });
        if (response && response.ok) {
            loadTodos();
            loadStats();
            
            // Broadcast to other tabs
            broadcastToLocalStorage('task.updated', { id: todoId, status: 'pending' });
        } else {
            showToast('Task pending nahi hua', 'error');
        }
    } catch (error) {
        console.error('Error marking pending:', error);
        showToast('Task pending nahi hua', 'error');
    }
}

async function deleteTodo(todoId) {
    // Confirmation dialog with Roman Urdu (Phase 7)
    if (!await confirmDialog('Kya aap is task ko delete karna chahte hain? Yeh action reversible nahi hai.')) {
        return;
    }

    try {
        const response = await apiRequest(`/api/todos/${todoId}`, { method: 'DELETE' });
        if (response && response.ok) {
            loadTodos();
            loadStats();
            
            // Broadcast to other tabs
            broadcastToLocalStorage('task.deleted', { id: todoId });
            
            showToast('Task delete ho gaya!', 'success');
        } else {
            showToast('Task delete nahi hua', 'error');
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
        showToast('Task delete nahi hua', 'error');
    }
}

async function editTodo(todoId) {
    const todo = currentTodos.find(t => t.id === todoId);
    if (!todo) return;

    document.getElementById('modalTitle').textContent = 'Edit Todo';
    document.getElementById('todoId').value = todo.id;
    document.getElementById('todoTitle').value = todo.title;
    document.getElementById('todoDescription').value = todo.description || '';
    document.getElementById('todoPriority').value = todo.priority;
    document.getElementById('todoDueDate').value = todo.due_date ? new Date(todo.due_date).toISOString().slice(0, 16) : '';
    document.getElementById('todoCategory').value = todo.category_id || '';
    
    // Hide recurring options for edit (recurring tasks can't be edited as recurring)
    document.getElementById('todoRecurring').checked = false;
    document.getElementById('recurrenceOptions').style.display = 'none';
    
    document.getElementById('todoModal').style.display = 'block';
}

/**
 * Helper: Format date
 * Roman Urdu: Date format karna
 */
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Helper: Escape HTML
 * Roman Urdu: HTML escape karna (XSS prevention)
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Helper: Debounce function
 * Roman Urdu: Function debounce karna
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modals = [document.getElementById('todoModal'), document.getElementById('categoryModal')];
    modals.forEach(modal => {
        if (modal && event.target === modal) {
            modal.style.display = 'none';
        }
    });
};
