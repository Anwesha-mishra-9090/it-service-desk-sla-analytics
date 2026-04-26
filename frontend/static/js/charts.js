/**
 * Charts.js - Chart configurations and utilities for IT Service Desk Dashboard
 * Uses Chart.js library for data visualization
 */

// Color palettes
const COLORS = {
    primary: '#007bff',
    success: '#28a745',
    danger: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8',
    dark: '#343a40',
    light: '#f8f9fa',
    
    category: {
        Network: '#007bff',
        Software: '#28a745',
        Hardware: '#ffc107'
    },
    
    priority: {
        High: '#dc3545',
        Medium: '#ffc107',
        Low: '#28a745'
    },
    
    sla: {
        'Within SLA': '#28a745',
        'Near Breach': '#ffc107',
        'Breached': '#dc3545'
    },
    
    status: {
        'Open': '#dc3545',
        'In Progress': '#ffc107',
        'Resolved': '#28a745',
        'Closed': '#6c757d'
    }
};

// Common chart options
const commonOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                font: {
                    size: 12
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0,0,0,0.8)',
            titleFont: {
                size: 14
            },
            bodyFont: {
                size: 12
            }
        }
    }
};

// Bar chart options
const barOptions = {
    ...commonOptions,
    scales: {
        y: {
            beginAtZero: true,
            grid: {
                drawBorder: true,
                color: 'rgba(0,0,0,0.1)'
            },
            title: {
                display: true,
                text: 'Number of Tickets'
            }
        },
        x: {
            grid: {
                display: false
            },
            title: {
                display: true,
                text: 'Category'
            }
        }
    }
};

// Pie/Doughnut chart options
const pieOptions = {
    ...commonOptions,
    plugins: {
        ...commonOptions.plugins,
        tooltip: {
            callbacks: {
                label: function(context) {
                    const label = context.label || '';
                    const value = context.raw || 0;
                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = ((value / total) * 100).toFixed(1);
                    return `${label}: ${value} (${percentage}%)`;
                }
            }
        }
    }
};

// Line chart options
const lineOptions = {
    ...commonOptions,
    scales: {
        y: {
            beginAtZero: true,
            title: {
                display: true,
                text: 'Number of Tickets'
            },
            grid: {
                color: 'rgba(0,0,0,0.1)'
            }
        },
        x: {
            title: {
                display: true,
                text: 'Date'
            },
            grid: {
                display: false
            }
        }
    },
    elements: {
        line: {
            tension: 0.4
        },
        point: {
            radius: 4,
            hoverRadius: 6
        }
    }
};

// Create Category Distribution Chart (Pie)
function createCategoryChart(data) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    const chartData = {
        labels: Object.keys(data),
        datasets: [{
            data: Object.values(data),
            backgroundColor: Object.keys(data).map(cat => COLORS.category[cat] || COLORS.primary),
            borderWidth: 2,
            borderColor: '#fff'
        }]
    };
    
    return new Chart(ctx, {
        type: 'pie',
        data: chartData,
        options: pieOptions
    });
}

// Create Priority Distribution Chart (Doughnut)
function createPriorityChart(data) {
    const ctx = document.getElementById('priorityChart').getContext('2d');
    
    const chartData = {
        labels: Object.keys(data),
        datasets: [{
            data: Object.values(data),
            backgroundColor: Object.keys(data).map(priority => COLORS.priority[priority] || COLORS.primary),
            borderWidth: 2,
            borderColor: '#fff'
        }]
    };
    
    return new Chart(ctx, {
        type: 'doughnut',
        data: chartData,
        options: pieOptions
    });
}

// Create SLA Status Chart (Bar)
function createSLAChart(data) {
    const ctx = document.getElementById('slaChart').getContext('2d');
    
    const chartData = {
        labels: ['Within SLA', 'Near Breach', 'Breached'],
        datasets: [{
            label: 'Number of Tickets',
            data: [data.within_sla, data.near_breach, data.breached],
            backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
            borderColor: '#fff',
            borderWidth: 2
        }]
    };
    
    return new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            ...barOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Tickets'
                    }
                }
            }
        }
    });
}

// Create Status Distribution Chart (Horizontal Bar)
function createStatusChart(data) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    
    const chartData = {
        labels: Object.keys(data),
        datasets: [{
            label: 'Tickets by Status',
            data: Object.values(data),
            backgroundColor: Object.keys(data).map(status => COLORS.status[status] || COLORS.primary),
            borderColor: '#fff',
            borderWidth: 2
        }]
    };
    
    return new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: barOptions
    });
}

// Create Trends Chart (Line)
function createTrendsChart(data) {
    const ctx = document.getElementById('trendsChart').getContext('2d');
    
    const chartData = {
        labels: Object.keys(data),
        datasets: [{
            label: 'Tickets Created',
            data: Object.values(data),
            borderColor: COLORS.primary,
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            borderWidth: 3,
            fill: true,
            pointBackgroundColor: COLORS.primary,
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7
        }]
    };
    
    return new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: lineOptions
    });
}

// Create SLA Performance by Priority Chart (Grouped Bar)
function createSLAByPriorityChart(data) {
    const ctx = document.getElementById('slaByPriorityChart').getContext('2d');
    
    const chartData = {
        labels: ['High', 'Medium', 'Low'],
        datasets: [
            {
                label: 'Total Tickets',
                data: [data.High?.total || 0, data.Medium?.total || 0, data.Low?.total || 0],
                backgroundColor: COLORS.primary,
                borderColor: '#fff',
                borderWidth: 1
            },
            {
                label: 'SLA Compliant',
                data: [data.High?.compliant || 0, data.Medium?.compliant || 0, data.Low?.compliant || 0],
                backgroundColor: COLORS.success,
                borderColor: '#fff',
                borderWidth: 1
            }
        ]
    };
    
    const options = {
        ...barOptions,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Tickets'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Priority Level'
                }
            }
        }
    };
    
    return new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: options
    });
}

// Create Ticket Aging Chart
function createAgingChart(data) {
    const ctx = document.getElementById('agingChart').getContext('2d');
    
    const chartData = {
        labels: Object.keys(data),
        datasets: [{
            label: 'Open Tickets Age',
            data: Object.values(data),
            backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
            borderColor: '#fff',
            borderWidth: 2
        }]
    };
    
    const options = {
        ...pieOptions,
        plugins: {
            ...pieOptions.plugins,
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.raw || 0;
                        return `${label}: ${value} tickets`;
                    }
                }
            }
        }
    };
    
    return new Chart(ctx, {
        type: 'pie',
        data: chartData,
        options: options
    });
}

// Utility function to update all charts with new data
function updateAllCharts(dashboardData) {
    if (window.categoryChart) {
        window.categoryChart.data.datasets[0].data = Object.values(dashboardData.category_distribution);
        window.categoryChart.update();
    }
    
    if (window.priorityChart) {
        window.priorityChart.data.datasets[0].data = Object.values(dashboardData.priority_distribution);
        window.priorityChart.update();
    }
    
    if (window.slaChart) {
        window.slaChart.data.datasets[0].data = [
            dashboardData.sla_metrics.within_sla,
            dashboardData.sla_metrics.near_breach,
            dashboardData.sla_metrics.breached
        ];
        window.slaChart.update();
    }
    
    if (window.statusChart) {
        window.statusChart.data.datasets[0].data = Object.values(dashboardData.status_distribution);
        window.statusChart.update();
    }
    
    if (window.trendsChart) {
        window.trendsChart.data.labels = Object.keys(dashboardData.trends);
        window.trendsChart.data.datasets[0].data = Object.values(dashboardData.trends);
        window.trendsChart.update();
    }
    
    if (window.slaByPriorityChart && dashboardData.sla_by_priority) {
        window.slaByPriorityChart.data.datasets[0].data = [
            dashboardData.sla_by_priority.High?.total || 0,
            dashboardData.sla_by_priority.Medium?.total || 0,
            dashboardData.sla_by_priority.Low?.total || 0
        ];
        window.slaByPriorityChart.data.datasets[1].data = [
            dashboardData.sla_by_priority.High?.compliant || 0,
            dashboardData.sla_by_priority.Medium?.compliant || 0,
            dashboardData.sla_by_priority.Low?.compliant || 0
        ];
        window.slaByPriorityChart.update();
    }
    
    if (window.agingChart && dashboardData.ticket_aging) {
        window.agingChart.data.datasets[0].data = Object.values(dashboardData.ticket_aging);
        window.agingChart.update();
    }
}

// Export chart as image
function exportChartAsImage(chartId, filename) {
    const canvas = document.getElementById(chartId);
    if (!canvas) return;
    
    const link = document.createElement('a');
    link.download = filename || `${chartId}.png`;
    link.href = canvas.toDataURL();
    link.click();
}

// Export all charts as PDF (requires html2canvas and jspdf)
async function exportAllChartsToPDF() {
    // This requires additional libraries: html2canvas and jspdf
    // Uncomment and add libraries to use this feature
    /*
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF('landscape');
    const charts = ['categoryChart', 'priorityChart', 'slaChart', 'statusChart', 'trendsChart'];
    
    for (let i = 0; i < charts.length; i++) {
        const canvas = document.getElementById(charts[i]);
        if (canvas) {
            const imgData = canvas.toDataURL('image/png');
            if (i > 0) pdf.addPage();
            pdf.addImage(imgData, 'PNG', 10, 10, 280, 150);
        }
    }
    
    pdf.save('dashboard-charts.pdf');
    */
    console.log('PDF export requires html2canvas and jspdf libraries');
}

// Initialize all charts with empty data
function initializeEmptyCharts() {
    const emptyData = {
        category_distribution: { Network: 0, Software: 0, Hardware: 0 },
        priority_distribution: { High: 0, Medium: 0, Low: 0 },
        sla_metrics: { within_sla: 0, near_breach: 0, breached: 0 },
        status_distribution: { Open: 0, 'In Progress': 0, Resolved: 0, Closed: 0 },
        trends: {},
        sla_by_priority: {
            High: { total: 0, compliant: 0 },
            Medium: { total: 0, compliant: 0 },
            Low: { total: 0, compliant: 0 }
        },
        ticket_aging: { '0-24h': 0, '24-48h': 0, '48h+': 0 }
    };
    
    updateAllCharts(emptyData);
}

// Export functions for use in dashboard
window.chartUtils = {
    createCategoryChart,
    createPriorityChart,
    createSLAChart,
    createStatusChart,
    createTrendsChart,
    createSLAByPriorityChart,
    createAgingChart,
    updateAllCharts,
    exportChartAsImage,
    initializeEmptyCharts,
    COLORS
};