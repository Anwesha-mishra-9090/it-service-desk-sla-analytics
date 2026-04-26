// Main JavaScript for IT Service Desk

// Utility Functions
function formatDateTime(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function formatTimeAgo(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    
    if (diff < 60) return `${diff} seconds ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
    return `${Math.floor(diff / 86400)} days ago`;
}

function getStatusIcon(status) {
    const icons = {
        'Open': 'bi-exclamation-circle',
        'In Progress': 'bi-arrow-repeat',
        'Resolved': 'bi-check-circle',
        'Closed': 'bi-x-circle'
    };
    return icons[status] || 'bi-question-circle';
}

function getPriorityIcon(priority) {
    const icons = {
        'High': 'bi-arrow-up-circle',
        'Medium': 'bi-arrow-right-circle',
        'Low': 'bi-arrow-down-circle'
    };
    return icons[priority] || 'bi-circle';
}

// Chart Utilities
function createChart(ctx, type, data, options) {
    return new Chart(ctx, {
        type: type,
        data: data,
        options: options
    });
}

// Export Functions
function downloadReport(data, filename) {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Form Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;
    return re.test(phone);
}

// Local Storage Helpers
const Storage = {
    set(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    },
    get(key) {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    },
    remove(key) {
        localStorage.removeItem(key);
    },
    clear() {
        localStorage.clear();
    }
};

// Event Debouncer
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

// Export for use in other files
window.utils = {
    formatDateTime,
    formatDate,
    formatTimeAgo,
    getStatusIcon,
    getPriorityIcon,
    downloadReport,
    validateEmail,
    validatePhone,
    Storage,
    debounce
};