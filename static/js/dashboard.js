/**
 * dashboard.js - Chart.js dashboard visualizations.
 *
 * Provides initialization functions for:
 *   - Burnout Distribution Pie Chart
 *   - Attrition Distribution Bar Chart
 *   - Model Accuracy Comparison Chart
 *   - Salary vs Burnout Scatter Plot
 *   - Confusion Matrix visualization
 */

// ── Color Palette ──────────────────────────────────────────
const COLORS = {
    low: '#4caf50',
    medium: '#ff9800',
    high: '#f44336',
    stay: '#2196f3',
    leave: '#e91e63',
    primary: '#1a237e',
    primaryLight: '#3949ab',
    logistic: '#42a5f5',
    randomForest: '#66bb6a',
};

// ── Burnout Distribution Pie Chart ─────────────────────────
function initBurnoutPieChart(burnoutCounts) {
    const ctx = document.getElementById('burnoutPieChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Low', 'Medium', 'High'],
            datasets: [{
                data: [
                    burnoutCounts['Low'] || 0,
                    burnoutCounts['Medium'] || 0,
                    burnoutCounts['High'] || 0,
                ],
                backgroundColor: [COLORS.low, COLORS.medium, COLORS.high],
                borderWidth: 2,
                borderColor: '#ffffff',
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { padding: 16, font: { size: 13 } }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                            return `${context.label}: ${context.parsed} (${pct}%)`;
                        }
                    }
                }
            }
        }
    });
}

// ── Attrition Distribution Bar Chart ───────────────────────
function initAttritionBarChart(attritionCounts) {
    const ctx = document.getElementById('attritionBarChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Stay', 'Leave'],
            datasets: [{
                label: 'Employee Count',
                data: [
                    attritionCounts['Stay'] || 0,
                    attritionCounts['Leave'] || 0,
                ],
                backgroundColor: [COLORS.stay, COLORS.leave],
                borderRadius: 6,
                borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#f0f0f0' },
                    ticks: { font: { size: 12 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 13, weight: '600' } }
                }
            }
        }
    });
}

// ── Model Accuracy Comparison Chart ────────────────────────
function initAccuracyChart(metrics) {
    const ctx = document.getElementById('accuracyChart').getContext('2d');

    const burnoutLR = metrics.burnout_model?.logistic_regression?.accuracy || 0;
    const burnoutRF = metrics.burnout_model?.random_forest?.accuracy || 0;
    const attritionLR = metrics.attrition_model?.logistic_regression?.accuracy || 0;
    const attritionRF = metrics.attrition_model?.random_forest?.accuracy || 0;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Burnout - LR', 'Burnout - RF', 'Attrition - LR', 'Attrition - RF'],
            datasets: [{
                label: 'Accuracy',
                data: [burnoutLR, burnoutRF, attritionLR, attritionRF],
                backgroundColor: [
                    COLORS.logistic, COLORS.randomForest,
                    COLORS.logistic, COLORS.randomForest,
                ],
                borderRadius: 6,
                borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Accuracy: ${(context.parsed.y * 100).toFixed(2)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    grid: { color: '#f0f0f0' },
                    ticks: {
                        callback: function(value) { return (value * 100) + '%'; },
                        font: { size: 12 }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 11 } }
                }
            }
        }
    });
}

// ── Salary vs Burnout Scatter Plot ─────────────────────────
function initSalaryBurnoutChart(salaryBurnoutData) {
    const ctx = document.getElementById('salaryBurnoutChart').getContext('2d');

    // Group data by burnout level
    const groups = { Low: [], Medium: [], High: [] };
    // Sample data for performance (max 200 points per group)
    const sampled = salaryBurnoutData.sort(() => 0.5 - Math.random()).slice(0, 600);

    sampled.forEach(item => {
        const level = item.burnout;
        if (groups[level]) {
            groups[level].push({ x: item.salary, y: level === 'Low' ? 1 : level === 'Medium' ? 2 : 3 });
        }
    });

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Low Burnout',
                    data: groups['Low'],
                    backgroundColor: COLORS.low + '80',
                    pointRadius: 3,
                },
                {
                    label: 'Medium Burnout',
                    data: groups['Medium'],
                    backgroundColor: COLORS.medium + '80',
                    pointRadius: 3,
                },
                {
                    label: 'High Burnout',
                    data: groups['High'],
                    backgroundColor: COLORS.high + '80',
                    pointRadius: 3,
                },
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { padding: 12, font: { size: 12 } }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Salary ($)', font: { size: 12 } },
                    grid: { color: '#f0f0f0' },
                    ticks: {
                        callback: function(value) { return '$' + (value / 1000) + 'k'; },
                        font: { size: 11 }
                    }
                },
                y: {
                    title: { display: true, text: 'Burnout Level', font: { size: 12 } },
                    grid: { color: '#f0f0f0' },
                    ticks: {
                        callback: function(value) {
                            return value === 1 ? 'Low' : value === 2 ? 'Medium' : value === 3 ? 'High' : '';
                        },
                        stepSize: 1,
                        font: { size: 11 }
                    },
                    min: 0,
                    max: 4,
                }
            }
        }
    });
}

// ── Confusion Matrix Chart ─────────────────────────────────
function initConfusionMatrixChart(metrics) {
    const ctx = document.getElementById('confusionMatrixChart').getContext('2d');

    // Get best burnout model's confusion matrix
    const bestModel = metrics.burnout_model?.best_model;
    const modelKey = bestModel === 'Random Forest' ? 'random_forest' : 'logistic_regression';
    const cm = metrics.burnout_model?.[modelKey]?.confusion_matrix;

    if (!cm || cm.length === 0) {
        ctx.font = '14px Segoe UI';
        ctx.fillStyle = '#757575';
        ctx.textAlign = 'center';
        ctx.fillText('No confusion matrix data available', ctx.canvas.width / 2, ctx.canvas.height / 2);
        return;
    }

    // Flatten confusion matrix for heatmap-style bar chart
    const labels = cm.length === 3 ? ['High', 'Low', 'Medium'] : ['Class 0', 'Class 1'];
    const dataFlat = [];
    const bgColors = [];
    const barLabels = [];

    for (let i = 0; i < cm.length; i++) {
        for (let j = 0; j < cm[i].length; j++) {
            barLabels.push(`Actual: ${labels[i]}\nPred: ${labels[j]}`);
            dataFlat.push(cm[i][j]);
            bgColors.push(i === j ? '#4caf50' : '#ef5350');
        }
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: barLabels,
            datasets: [{
                label: 'Count',
                data: dataFlat,
                backgroundColor: bgColors,
                borderRadius: 4,
                borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: `Best Model: ${bestModel || 'N/A'}`,
                    font: { size: 12 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#f0f0f0' },
                    title: { display: true, text: 'Count' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 9 }, maxRotation: 45 }
                }
            }
        }
    });
}

// ── Utility Functions ──────────────────────────────────────

function toggleNav() {
    document.querySelector('.nav-links').classList.toggle('nav-open');
}

function showLoading(element, text) {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    if (overlay) {
        overlay.style.display = 'flex';
        if (loadingText) loadingText.textContent = text || 'Processing...';
    }
}

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function() { alert.remove(); }, 300);
        }, 5000);
    });
});
