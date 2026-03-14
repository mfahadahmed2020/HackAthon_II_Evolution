/**
 * Analytics Module
 * Roman Urdu: Productivity analytics - stats, trends, aur category breakdown
 * 
 * Features:
 * - loadAnalyticsStats(): Current productivity stats load karna
 * - loadWeeklyTrends(): Weekly trends chart render karna
 * - loadCategoryBreakdown(): Category-wise breakdown render karna
 * - Auto-refresh every 30 seconds
 * 
 * API Endpoints:
 * - GET /api/analytics/stats - Current stats
 * - GET /api/analytics/weekly - Weekly trends
 * - GET /api/analytics/monthly - Monthly trends
 */

// Global analytics data cache
let analyticsData = null;
let autoRefreshInterval = null;

/**
 * Load analytics stats from API
 * Roman Urdu: Current productivity stats API se load karna
 */
async function loadAnalyticsStats() {
    try {
        const response = await apiRequest('/api/analytics/stats');
        if (!response) {
            console.error('Failed to load analytics: No response');
            return null;
        }

        const stats = await response.json();
        analyticsData = stats;
        
        // Update stats cards
        updateStatsCards(stats);
        
        // Update category breakdown
        if (stats.categories_breakdown) {
            updateCategoryBreakdown(stats.categories_breakdown);
        }
        
        return stats;
    } catch (error) {
        console.error('Error loading analytics stats:', error);
        // Silent fail for analytics - don't show toast on every refresh
        return null;
    }
}

/**
 * Update stats cards in UI
 * Roman Urdu: Stats cards ko update karna
 * 
 * @param {Object} stats - Analytics stats data
 */
function updateStatsCards(stats) {
    // Update total
    const totalEl = document.getElementById('analyticsTotal');
    if (totalEl) {
        animateNumber(totalEl, parseInt(totalEl.textContent) || 0, stats.total || 0, 500);
    }
    
    // Update completed
    const completedEl = document.getElementById('analyticsCompleted');
    if (completedEl) {
        animateNumber(completedEl, parseInt(completedEl.textContent) || 0, stats.completed || 0, 500);
    }
    
    // Update pending
    const pendingEl = document.getElementById('analyticsPending');
    if (pendingEl) {
        animateNumber(pendingEl, parseInt(pendingEl.textContent) || 0, stats.pending || 0, 500);
    }
    
    // Update streak
    const streakEl = document.getElementById('analyticsStreak');
    if (streakEl) {
        streakEl.textContent = `${stats.current_streak || 0} days`;
    }
    
    // Update completion rate
    const rateEl = document.getElementById('analyticsCompletionRate');
    if (rateEl) {
        rateEl.textContent = `${(stats.completion_percentage || 0).toFixed(1)}%`;
    }
    
    // Update longest streak
    const longestStreakEl = document.getElementById('analyticsLongestStreak');
    if (longestStreakEl) {
        longestStreakEl.textContent = `${stats.longest_streak || 0} days`;
    }
}

/**
 * Load weekly trends
 * Roman Urdu: Weekly trends load karna aur chart render karna
 */
async function loadWeeklyTrends() {
    try {
        const response = await apiRequest('/api/analytics/weekly?weeks=4');
        if (!response) {
            console.error('Failed to load weekly trends: No response');
            return null;
        }

        const data = await response.json();
        
        // Render chart
        renderWeeklyTrendsChart(data.weeks || []);
        
        return data;
    } catch (error) {
        console.error('Error loading weekly trends:', error);
        return null;
    }
}

/**
 * Render weekly trends chart (simple CSS-based bar chart)
 * Roman Urdu: Weekly trends ka simple bar chart render karna
 * 
 * @param {Array} weeks - Weekly trends data
 */
function renderWeeklyTrendsChart(weeks) {
    const container = document.getElementById('weeklyTrendsChart');
    if (!container) return;
    
    if (!weeks || weeks.length === 0) {
        container.innerHTML = '<p class="empty-message">No trends data available</p>';
        return;
    }
    
    // Find max completion rate for scaling
    const maxRate = Math.max(...weeks.map(w => w.completion_rate), 100);
    
    // Create chart HTML
    const chartHTML = `
        <div class="bar-chart">
            <div class="bar-chart-bars">
                ${weeks.map(week => {
                    const height = (week.completion_rate / maxRate) * 100;
                    const weekStart = new Date(week.week_start);
                    const weekEnd = new Date(week.week_end);
                    const dateLabel = weekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                    
                    return `
                        <div class="bar-item">
                            <div class="bar-wrapper">
                                <div class="bar-fill" style="height: ${height}%;" 
                                     title="${week.completed}/${week.total} completed">
                                    <span class="bar-value">${week.completion_rate.toFixed(0)}%</span>
                                </div>
                            </div>
                            <div class="bar-label">${dateLabel}</div>
                            <div class="bar-stats">
                                <span class="stat-completed">✓ ${week.completed}</span>
                                <span class="stat-pending">○ ${week.pending}</span>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
    `;
    
    container.innerHTML = chartHTML;
}

/**
 * Update category breakdown
 * Roman Urdu: Category-wise breakdown update karna
 * 
 * @param {Array} breakdown - Category breakdown data
 */
function updateCategoryBreakdown(breakdown) {
    const container = document.getElementById('categoryBreakdownContainer');
    if (!container) return;
    
    if (!breakdown || breakdown.length === 0) {
        container.innerHTML = '<p class="empty-message">No categories yet. Create one to see breakdown!</p>';
        return;
    }
    
    // Create breakdown HTML
    const breakdownHTML = `
        <div class="category-breakdown-list">
            ${breakdown.map(cat => {
                const width = cat.completion_rate || 0;
                return `
                    <div class="category-breakdown-item">
                        <div class="category-breakdown-header">
                            <span class="category-color-badge" style="background-color: ${cat.category_color};"></span>
                            <span class="category-name">${escapeHtml(cat.category_name)}</span>
                            <span class="category-rate">${cat.completion_rate.toFixed(1)}%</span>
                        </div>
                        <div class="category-progress-bar">
                            <div class="category-progress-fill" 
                                 style="width: ${width}%; background-color: ${cat.category_color};">
                            </div>
                        </div>
                        <div class="category-breakdown-stats">
                            <span>✓ ${cat.completed} completed</span>
                            <span>○ ${cat.pending} pending</span>
                            <span>📊 ${cat.total} total</span>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
    
    container.innerHTML = breakdownHTML;
}

/**
 * Animate number
 * Roman Urdu: Number ko animate karna (counting effect)
 * 
 * @param {HTMLElement} element - Element to update
 * @param {number} start - Starting value
 * @param {number} end - Ending value
 * @param {number} duration - Animation duration in ms
 */
function animateNumber(element, start, end, duration = 500) {
    if (!element) return;
    
    const range = end - start;
    const increment = range / (duration / 16); // 60 FPS
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

/**
 * Start auto-refresh
 * Roman Urdu: Auto-refresh start karna (every 30 seconds)
 */
function startAutoRefresh() {
    // Clear existing interval
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    // Set new interval (30 seconds)
    autoRefreshInterval = setInterval(() => {
        loadAnalyticsStats();
    }, 30000);
    
    console.log('Analytics auto-refresh started (30s interval)');
}

/**
 * Stop auto-refresh
 * Roman Urdu: Auto-refresh stop karna
 */
function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        console.log('Analytics auto-refresh stopped');
    }
}

/**
 * Manual refresh
 * Roman Urdu: Manual refresh button handler
 */
function refreshAnalytics() {
    showLoading(true);
    Promise.all([
        loadAnalyticsStats(),
        loadWeeklyTrends()
    ]).finally(() => {
        showLoading(false);
        showToast('Analytics refreshed!', 'success');
    });
}

/**
 * Initialize analytics module
 * Roman Urdu: Analytics module initialize karna on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    // Load initial data
    loadAnalyticsStats();
    loadWeeklyTrends();
    
    // Start auto-refresh
    startAutoRefresh();
    
    // Add refresh button if not exists
    const statsContainer = document.getElementById('analyticsStatsContainer');
    if (statsContainer && !document.getElementById('refreshAnalyticsBtn')) {
        const refreshBtn = document.createElement('button');
        refreshBtn.id = 'refreshAnalyticsBtn';
        refreshBtn.className = 'btn btn-secondary btn-sm';
        refreshBtn.textContent = '⟳ Refresh';
        refreshBtn.onclick = refreshAnalytics;
        refreshBtn.style.cssText = 'margin-left: auto;';
        statsContainer.appendChild(refreshBtn);
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopAutoRefresh();
});

// Export functions
window.AnalyticsModule = {
    loadAnalyticsStats,
    loadWeeklyTrends,
    refreshAnalytics,
    startAutoRefresh,
    stopAutoRefresh
};
