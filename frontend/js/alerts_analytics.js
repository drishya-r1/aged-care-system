// Loads and displays weekly alert analytics in a bar chart
async function loadAlertsAnalytics() {
    const analyticsDiv = document.getElementById('alertsAnalytics');
    if (!analyticsDiv) return;
    try {
        const res = await fetch('/api/analytics/alerts_weekly');
        const data = await res.json();
        const labels = data.weekly_alerts.map(d => d.date);
        const counts = data.weekly_alerts.map(d => d.count);
        // Remove previous chart if exists
        analyticsDiv.innerHTML = '<canvas id="alertsChart" style="max-width:700px;"></canvas>';
        const ctx = document.getElementById('alertsChart').getContext('2d');
        if (window.alertsChartInstance) window.alertsChartInstance.destroy();
        window.alertsChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Alerts Reported (Last 7 Days)',
                    data: counts,
                    backgroundColor: '#1976d2',
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'Alerts Reported This Week' }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        precision: 0,
                        ticks: {
                            stepSize: 5 // Show y-axis ticks at 0, 5, 10, 15, etc.
                        }
                    }
                }
            }
        });
    } catch (e) {
        analyticsDiv.innerHTML = '<div style="color:#d32f2f;">Failed to load analytics.</div>';
    }
}
