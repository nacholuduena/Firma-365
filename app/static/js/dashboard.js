// ── Time update ──────────────────────────────────────────
function updateTime() {
    const el = document.getElementById('current-time');
    if (el) {
        el.textContent = new Date().toLocaleString('es-AR', {
            dateStyle: 'medium', timeStyle: 'short'
        });
    }
}
updateTime();
setInterval(updateTime, 60000);

// ── Sidebar toggle (mobile) ─────────────────────────────
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('show');
}

// ── Chart.js defaults ───────────────────────────────────
Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding = 16;

const COLORS = {
    primary: '#1a73e8',
    success: '#34a853',
    warning: '#fbbc04',
    danger: '#ea4335',
    info: '#4285f4',
    purple: '#9334e6',
    teal: '#00bcd4',
    orange: '#ff9800',
    palette: ['#1a73e8', '#34a853', '#fbbc04', '#ea4335', '#9334e6', '#00bcd4', '#ff9800', '#e91e63'],
};

// ── Chart helpers ────────────────────────────────────────
function createDoughnut(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || COLORS.palette,
                borderWidth: 2,
                borderColor: '#fff',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function createBar(canvasId, labels, datasets, horizontal) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    return new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: horizontal ? 'y' : 'x',
            scales: {
                x: { grid: { display: false } },
                y: { grid: { color: '#f0f0f0' } },
            },
            plugins: {
                legend: { display: datasets.length > 1 }
            }
        }
    });
}

function createLine(canvasId, labels, datasets) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    return new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false } },
                y: { grid: { color: '#f0f0f0' }, beginAtZero: true },
            },
            plugins: {
                legend: { display: datasets.length > 1 }
            },
            elements: {
                line: { tension: 0.3 },
                point: { radius: 3 }
            }
        }
    });
}

// ── Number formatting ────────────────────────────────────
function formatNumber(n, decimals) {
    if (n === null || n === undefined) return '-';
    return n.toLocaleString('es-AR', {
        minimumFractionDigits: decimals || 0,
        maximumFractionDigits: decimals || 0,
    });
}

function formatCurrency(n) {
    if (n === null || n === undefined) return '-';
    return '$' + n.toLocaleString('es-AR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

// ── Auto-refresh ─────────────────────────────────────────
function autoRefresh(intervalMs) {
    if (intervalMs && intervalMs > 0) {
        setTimeout(() => location.reload(), intervalMs);
    }
}
