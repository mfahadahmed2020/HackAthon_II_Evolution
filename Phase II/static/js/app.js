// Global utility functions

function getToken() {
    return localStorage.getItem('token');
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}

async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(endpoint, {
        ...options,
        headers
    });
    
    if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
        return null;
    }
    
    return response;
}
