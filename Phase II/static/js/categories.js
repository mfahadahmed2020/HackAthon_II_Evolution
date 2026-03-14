/**
 * Category Management Module
 * Roman Urdu: Category CRUD operations - users apne tasks ko organize karne ke liye categories bana sakte hain
 * 
 * Features:
 * - loadCategories(): Saare categories load karna
 * - createCategory(name, color): Naya category create karna
 * - updateCategory(id, name, color): Category update karna
 * - deleteCategory(id): Category delete karna (confirm dialog ke saath)
 * 
 * Error Messages (Roman Urdu):
 * - "Category pehle se मौजूद hai" - Duplicate category name
 * - "Category nahi mili" - Category not found
 * - "Category create nahi hui" - Create failed
 */

// Global categories cache
let categoriesCache = [];

/**
 * Load all categories from API
 * Roman Urdu: Saare categories API se load karna
 */
async function loadCategories() {
    try {
        const response = await apiRequest('/api/categories');
        if (!response) {
            console.error('Failed to load categories: No response');
            return [];
        }

        const data = await response.json();
        categoriesCache = data.categories || [];
        
        // Update category dropdown in todo modal
        updateCategoryDropdown();
        
        // Update category filter buttons
        updateCategoryFilters();
        
        // Update category list in category modal
        updateCategoryList();
        
        return categoriesCache;
    } catch (error) {
        console.error('Error loading categories:', error);
        showToast('Categories load nahi huin', 'error');
        return [];
    }
}

/**
 * Update category dropdown in todo form
 * Roman Urdu: Todo form mein category dropdown update karna
 */
function updateCategoryDropdown() {
    const select = document.getElementById('todoCategory');
    if (!select) return;
    
    // Keep the first "No Category" option
    select.innerHTML = '<option value="">No Category</option>';
    
    categoriesCache.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        option.style.color = category.color;
        select.appendChild(option);
    });
}

/**
 * Update category filter buttons
 * Roman Urdu: Category filter buttons update karna
 */
function updateCategoryFilters() {
    const container = document.getElementById('categoryFiltersContainer');
    if (!container) return;
    
    // Remove existing category buttons (keep "All Categories" and "Add Category" button)
    const existingButtons = container.querySelectorAll('.category-filter-btn[data-category]');
    existingButtons.forEach(btn => btn.remove());
    
    // Add category buttons
    categoriesCache.forEach(category => {
        const button = document.createElement('button');
        button.className = 'category-filter-btn';
        button.dataset.category = category.id;
        button.innerHTML = `
            <span class="category-color-badge" style="background-color: ${category.color};"></span>
            ${category.name}
        `;
        button.onclick = () => filterByCategory(category.id, button);
        container.insertBefore(button, container.lastElementChild);
    });
}

/**
 * Update category list in category modal
 * Roman Urdu: Category modal mein categories ki list update karna
 */
function updateCategoryList() {
    const container = document.getElementById('categoryList');
    if (!container) return;
    
    if (categoriesCache.length === 0) {
        container.innerHTML = '<p class="empty-message">No categories yet. Create one!</p>';
        return;
    }
    
    container.innerHTML = categoriesCache.map(category => `
        <div class="category-item" data-id="${category.id}">
            <span class="category-color-badge" style="background-color: ${category.color};"></span>
            <span class="category-name">${escapeHtml(category.name)}</span>
            <div class="category-actions">
                <button class="btn-edit-sm" onclick="editCategory(${category.id})" title="Edit">✎</button>
                <button class="btn-delete-sm" onclick="deleteCategory(${category.id})" title="Delete">🗑</button>
            </div>
        </div>
    `).join('');
}

/**
 * Show category modal
 * Roman Urdu: Category modal show karna
 */
function showCategoryModal() {
    document.getElementById('categoryModalTitle').textContent = 'Add New Category';
    document.getElementById('categoryId').value = '';
    document.getElementById('categoryForm').reset();
    document.getElementById('categoryColor').value = '#4f46e5';
    document.getElementById('colorPreview').textContent = '#4f46e5';
    document.getElementById('categoryModal').style.display = 'block';
    
    // Load categories if not loaded
    if (categoriesCache.length === 0) {
        loadCategories();
    }
}

/**
 * Close category modal
 * Roman Urdu: Category modal close karna
 */
function closeCategoryModal() {
    document.getElementById('categoryModal').style.display = 'none';
}

/**
 * Create a new category
 * Roman Urdu: Naya category create karna
 * 
 * @param {string} name - Category name
 * @param {string} color - Hex color code (#RRGGBB)
 */
async function createCategory(name, color) {
    try {
        const response = await apiRequest('/api/categories', {
            method: 'POST',
            body: JSON.stringify({ name, color })
        });
        
        if (!response) {
            throw new Error('No response');
        }
        
        if (response.status === 400) {
            const error = await response.json();
            throw new Error(error.detail || 'Category pehle se मौजूद hai');
        }
        
        if (!response.ok) {
            throw new Error('Category create nahi hui');
        }
        
        const category = await response.json();
        showToast('Category create ho gayi!', 'success');
        
        // Reload categories
        await loadCategories();
        
        return category;
    } catch (error) {
        console.error('Error creating category:', error);
        showToast(error.message || 'Category create nahi hui', 'error');
        throw error;
    }
}

/**
 * Update an existing category
 * Roman Urdu: Existing category update karna
 * 
 * @param {number} id - Category ID
 * @param {string} name - New name
 * @param {string} color - New color
 */
async function updateCategory(id, name, color) {
    try {
        const response = await apiRequest(`/api/categories/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ name, color })
        });
        
        if (!response) {
            throw new Error('No response');
        }
        
        if (response.status === 400) {
            const error = await response.json();
            throw new Error(error.detail || 'Category pehle se मौजूद hai');
        }
        
        if (!response.ok) {
            throw new Error('Category update nahi hui');
        }
        
        const category = await response.json();
        showToast('Category update ho gayi!', 'success');
        
        // Reload categories
        await loadCategories();
        
        return category;
    } catch (error) {
        console.error('Error updating category:', error);
        showToast(error.message || 'Category update nahi hui', 'error');
        throw error;
    }
}

/**
 * Delete a category
 * Roman Urdu: Category delete karna (confirm dialog ke saath)
 * 
 * @param {number} id - Category ID
 */
async function deleteCategory(id) {
    // Confirm deletion
    if (!confirm('Kya aap is category ko delete karna chahte hain? Is category se jude tasks mein se category remove ho jayega.')) {
        return;
    }
    
    try {
        const response = await apiRequest(`/api/categories/${id}`, {
            method: 'DELETE'
        });
        
        if (!response) {
            throw new Error('No response');
        }
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Category nahi mili');
            }
            throw new Error('Category delete nahi hui');
        }
        
        showToast('Category delete ho gayi!', 'success');
        
        // Reload categories
        await loadCategories();
        
        // Reload todos to reflect changes
        if (typeof loadTodos === 'function') {
            loadTodos();
        }
    } catch (error) {
        console.error('Error deleting category:', error);
        showToast(error.message || 'Category delete nahi hui', 'error');
        throw error;
    }
}

/**
 * Edit a category (load into form)
 * Roman Urdu: Category ko edit karne ke liye form mein load karna
 * 
 * @param {number} id - Category ID
 */
function editCategory(id) {
    const category = categoriesCache.find(c => c.id === id);
    if (!category) return;
    
    document.getElementById('categoryId').value = category.id;
    document.getElementById('categoryName').value = category.name;
    document.getElementById('categoryColor').value = category.color;
    document.getElementById('colorPreview').textContent = category.color;
    document.getElementById('categoryModalTitle').textContent = 'Edit Category';
}

/**
 * Filter todos by category
 * Roman Urdu: Category ke basis par tasks filter karna
 * 
 * @param {number|string} categoryId - Category ID or 'all'
 * @param {HTMLElement} button - Clicked button element
 */
function filterByCategory(categoryId, button) {
    // Update active state
    document.querySelectorAll('.category-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');
    
    // Store current category filter
    window.currentCategoryFilter = categoryId;
    
    // Reload todos with category filter
    if (typeof loadTodos === 'function') {
        loadTodos();
    }
}

/**
 * Get category by ID
 * Roman Urdu: ID se category obtain karna
 * 
 * @param {number} id - Category ID
 * @returns {Object|null} Category object or null
 */
function getCategoryById(id) {
    return categoriesCache.find(c => c.id === id) || null;
}

/**
 * Initialize category module on page load
 * Roman Urdu: Page load par category module initialize karna
 */
document.addEventListener('DOMContentLoaded', () => {
    // Load categories
    loadCategories();
    
    // Setup category form
    const categoryForm = document.getElementById('categoryForm');
    if (categoryForm) {
        categoryForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const categoryId = document.getElementById('categoryId').value;
            const name = document.getElementById('categoryName').value.trim();
            const color = document.getElementById('categoryColor').value;
            
            if (!name) {
                showToast('Category name zaroori hai', 'error');
                return;
            }
            
            try {
                if (categoryId) {
                    // Update existing category
                    await updateCategory(parseInt(categoryId), name, color);
                } else {
                    // Create new category
                    await createCategory(name, color);
                }
                
                // Reset form
                categoryForm.reset();
                document.getElementById('categoryId').value = '';
            } catch (error) {
                // Error already shown by function
            }
        });
    }
    
    // Setup color picker preview
    const colorPicker = document.getElementById('categoryColor');
    const colorPreview = document.getElementById('colorPreview');
    if (colorPicker && colorPreview) {
        colorPicker.addEventListener('input', (e) => {
            colorPreview.textContent = e.target.value;
        });
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('categoryModal');
    if (event.target === modal) {
        closeCategoryModal();
    }
};
