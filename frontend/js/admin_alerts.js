// admin_alerts.js: Loads alerts and food requests for admin dashboard
async function loadAdminAlerts() {
    console.log('loadAdminAlerts called');
    const alertsTbody = document.getElementById('alertsTbody');
    const foodAlertsTbody = document.getElementById('foodAlertsTbody');
    if (!alertsTbody || !foodAlertsTbody) {
        console.log('alertsTbody or foodAlertsTbody not found');
        return;
    }
    // Resident Alerts
    try {
        const res = await fetch('/api/nurse/alerts?units=all');
        console.log('Requested /api/nurse/alerts?units=all, status:', res.status);
        const data = await res.json();
        console.log('Alerts data:', data);
        alertsTbody.innerHTML = '';
        if (data.alerts && data.alerts.length > 0) {
            data.alerts.forEach(alert => {
                const isEmergency = alert.alert_type && alert.alert_type.toLowerCase() === 'emergency';
                alertsTbody.innerHTML += `
                    <tr>
                        <td>${alert.alert_id}</td>
                        <td style="color:${isEmergency ? '#d32f2f' : '#1976d2'};font-weight:bold;">${alert.alert_type || ''}</td>
                        <td>${alert.details || ''}</td>
                        <td>${alert.unit || ''}</td>
                        <td>${alert.status}</td>
                        <td>
                            <button class="attend-btn" data-id="${alert.alert_id}" ${alert.status === 'Attended' ? 'disabled' : ''}>
                                Attend
                            </button>
                        </td>
                    </tr>
                `;
            });
        } else {
            alertsTbody.innerHTML = '<tr><td colspan="6">No alerts found.</td></tr>';
        }
    } catch (e) {
        console.error('Failed to load alerts:', e);
        alertsTbody.innerHTML = '<tr><td colspan="6">Failed to load alerts.</td></tr>';
    }
    // Food Requests
    try {
        const res = await fetch('/api/nurse/food_alerts?units=all');
        console.log('Requested /api/nurse/food_alerts?units=all, status:', res.status);
        const data = await res.json();
        console.log('Food alerts data:', data);
        foodAlertsTbody.innerHTML = '';
        if (data.food_alerts && data.food_alerts.length > 0) {
            data.food_alerts.forEach(alert => {
                foodAlertsTbody.innerHTML += `
                    <tr>
                        <td>${alert.alert_id}</td>
                        <td>${alert.details || ''}</td>
                        <td>${alert.unit || ''}</td>
                        <td>${alert.status}</td>
                        <td>
                            <button class="attend-btn" data-id="${alert.alert_id}" ${alert.status === 'Attended' ? 'disabled' : ''}>
                                Attend
                            </button>
                        </td>
                    </tr>
                `;
            });
        } else {
            foodAlertsTbody.innerHTML = '<tr><td colspan="5">No food requests found.</td></tr>';
        }
    } catch (e) {
        console.error('Failed to load food requests:', e);
        foodAlertsTbody.innerHTML = '<tr><td colspan="5">Failed to load food requests.</td></tr>';
    }
}

// Remove export for browser compatibility
// Only export loadAdminAlerts for use in admin.html
// export { loadAdminAlerts };
