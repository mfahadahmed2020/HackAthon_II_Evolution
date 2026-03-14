/**
 * UI Utilities Module
 * Roman Urdu: UI helper functions - Toast notifications, loading states, confirmation dialogs
 * 
 * Features:
 * - showToast(message, type): Toast notification show karna
 * - showLoading(show): Loading overlay show/hide karna
 * - confirmDialog(message): Confirmation dialog with Roman Urdu messages
 * - escapeHtml(text): HTML injection se bachne ke liye text escape karna
 * - showValidationError(element, message): Form validation error show karna
 */

/**
 * Show toast notification
 * Roman Urdu: Toast notification show karna (auto-dismiss after 5 seconds)
 * 
 * @param {string} message - Notification message
 * @param {string} type - Type: 'success', 'error', 'warning', 'info'
 * @param {number} duration - Auto-dismiss duration in ms (default: 5000)
 */
function showToast(message, type = 'info', duration = 5000) {
    const container = document.getElementById('toastContainer');
    if (!container) {
        console.warn('Toast container not found');
        return;
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${getToastIcon(type)}</span>
        <span class="toast-message">${escapeHtml(message)}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Add to container
    container.appendChild(toast);
    
    // Auto-dismiss after duration
    if (duration > 0) {
        setTimeout(() => {
            toast.classList.add('toast-hiding');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
    
    // Play sound for error notifications
    if (type === 'error') {
        playErrorSound();
    }
}

/**
 * Get toast icon based on type
 * Roman Urdu: Type ke basis par toast icon return karna
 */
function getToastIcon(type) {
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };
    return icons[type] || icons.info;
}

/**
 * Play error sound (optional)
 * Roman Urdu: Error sound play karna (optional feature)
 */
function playErrorSound() {
    // Optional: Add error sound effect
    // Can be implemented using Web Audio API or HTML5 Audio
    // For now, silent
}

/**
 * Show/hide loading overlay
 * Roman Urdu: Loading overlay show/hide karna
 * 
 * @param {boolean} show - true to show, false to hide
 */
function showLoading(show = true) {
    const overlay = document.getElementById('loadingOverlay');
    if (!overlay) return;
    
    if (show) {
        overlay.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    } else {
        overlay.style.display = 'none';
        document.body.style.overflow = ''; // Restore scrolling
    }
}

/**
 * Show validation error
 * Roman Urdu: Form validation error show karna
 * 
 * @param {HTMLElement} element - Input element
 * @param {string} message - Error message
 */
function showValidationError(element, message) {
    if (!element) return;
    
    // Add error class
    element.classList.add('input-error');
    
    // Remove existing error message
    const existingError = element.parentElement.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    element.parentElement.appendChild(errorDiv);
    
    // Remove error on input
    element.addEventListener('input', function clearError() {
        element.classList.remove('input-error');
        const err = element.parentElement.querySelector('.error-message');
        if (err) err.remove();
        element.removeEventListener('input', clearError);
    }, { once: true });
}

/**
 * Clear validation errors
 * Roman Urdu: Validation errors clear karna
 * 
 * @param {HTMLFormElement} form - Form element
 */
function clearValidationErrors(form) {
    if (!form) return;
    
    // Remove error class from all inputs
    form.querySelectorAll('.input-error').forEach(el => {
        el.classList.remove('input-error');
    });
    
    // Remove error messages
    form.querySelectorAll('.error-message').forEach(el => {
        el.remove();
    });
}

/**
 * Validate form field
 * Roman Urdu: Form field validate karna
 * 
 * @param {HTMLElement} element - Input element
 * @param {Object} rules - Validation rules
 * @returns {boolean} true if valid
 */
function validateField(element, rules = {}) {
    const value = element.value.trim();
    const fieldName = element.parentElement.querySelector('label')?.textContent || 'Field';
    
    // Required validation
    if (rules.required && !value) {
        showValidationError(element, `${fieldName} zaroori hai`);
        return false;
    }
    
    // Min length validation
    if (rules.minLength && value.length < rules.minLength) {
        showValidationError(element, `${fieldName} kam se kam ${rules.minLength} characters hona chahiye`);
        return false;
    }
    
    // Max length validation
    if (rules.maxLength && value.length > rules.maxLength) {
        showValidationError(element, `${fieldName} zyada se zyada ${rules.maxLength} characters ho sakte hain`);
        return false;
    }
    
    // Email validation
    if (rules.email && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showValidationError(element, 'Invalid email address');
            return false;
        }
    }
    
    // Number validation
    if (rules.number && value) {
        if (isNaN(value)) {
            showValidationError(element, `${fieldName} number hona chahiye`);
            return false;
        }
    }
    
    // Range validation
    if (rules.min !== undefined && value < rules.min) {
        showValidationError(element, `${fieldName} kam se kam ${rules.min} hona chahiye`);
        return false;
    }
    
    if (rules.max !== undefined && value > rules.max) {
        showValidationError(element, `${fieldName} zyada se zyada ${rules.max} ho sakta hai`);
        return false;
    }
    
    return true;
}

/**
 * Validate entire form
 * Roman Urdu: Pure form ko validate karna
 * 
 * @param {HTMLFormElement} form - Form element
 * @param {Object} fieldRules - Field validation rules
 * @returns {boolean} true if all valid
 */
function validateForm(form, fieldRules = {}) {
    if (!form) return false;
    
    clearValidationErrors(form);
    
    let isValid = true;
    
    // Validate each field with rules
    Object.keys(fieldRules).forEach(fieldName => {
        const element = form.querySelector(`[name="${fieldName}"]`) || 
                       form.querySelector(`#${fieldName}`);
        if (element) {
            const fieldValid = validateField(element, fieldRules[fieldName]);
            if (!fieldValid) {
                isValid = false;
            }
        }
    });
    
    // Also validate required fields without explicit rules
    form.querySelectorAll('[required]').forEach(element => {
        const fieldValid = validateField(element, { required: true });
        if (!fieldValid) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Show confirmation dialog
 * Roman Urdu: Confirmation dialog with Roman Urdu messages
 * 
 * @param {string} message - Confirmation message
 * @returns {Promise<boolean>} true if confirmed
 */
function confirmDialog(message) {
    return new Promise((resolve) => {
        const confirmed = confirm(message);
        resolve(confirmed);
    });
}

/**
 * Format date for display
 * Roman Urdu: Date ko display format mein convert karna
 * 
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted date
 */
function formatDate(date) {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Format relative time
 * Roman Urdu: Time ko relative format mein (e.g., "2 hours ago")
 * 
 * @param {string|Date} date - Date to format
 * @returns {string} Relative time string
 */
function formatRelativeTime(date) {
    if (!date) return '';
    
    const d = new Date(date);
    const now = new Date();
    const diffMs = now - d;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) {
        return 'Just now';
    } else if (diffMins < 60) {
        return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
        return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    } else if (diffDays < 7) {
        return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    } else {
        return formatDate(date);
    }
}

/**
 * Animate element
 * Roman Urdu: Element ko animate karna
 * 
 * @param {HTMLElement} element - Element to animate
 * @param {string} animation - Animation class
 */
function animateElement(element, animation) {
    if (!element) return;
    
    element.classList.add(animation);
    setTimeout(() => {
        element.classList.remove(animation);
    }, 500);
}

/**
 * Flash element (visual feedback)
 * Roman Urdu: Element ko flash karna (real-time update feedback)
 * 
 * @param {HTMLElement} element - Element to flash
 */
function flashElement(element) {
    if (!element) return;
    
    element.classList.add('flash-animation');
    setTimeout(() => {
        element.classList.remove('flash-animation');
    }, 1000);
}

/**
 * Scroll to element smoothly
 * Roman Urdu: Element par smoothly scroll karna
 * 
 * @param {HTMLElement} element - Target element
 */
function scrollToElement(element) {
    if (!element) return;
    
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
    });
}

/**
 * Copy to clipboard
 * Roman Urdu: Text ko clipboard mein copy karna
 * 
 * @param {string} text - Text to copy
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
    } catch (error) {
        console.error('Failed to copy:', error);
        showToast('Copy failed', 'error');
    }
}

/**
 * Debounce function
 * Roman Urdu: Function ko debounce karna (performance optimization)
 * 
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
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

/**
 * Throttle function
 * Roman Urdu: Function ko throttle karna (rate limiting)
 * 
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in ms
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for use in other modules
window.UIUtils = {
    showToast,
    showLoading,
    showValidationError,
    clearValidationErrors,
    validateField,
    validateForm,
    confirmDialog,
    formatDate,
    formatRelativeTime,
    animateElement,
    flashElement,
    scrollToElement,
    copyToClipboard,
    debounce,
    throttle,
    escapeHtml
};
