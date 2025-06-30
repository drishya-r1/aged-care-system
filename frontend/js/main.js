// This file contains the Java Script code for the frontend application. It handles user interactions, such as button clicks for alerts and assistance requests, and communicates with the backend API.

document.addEventListener('DOMContentLoaded', function() {
    // Button references
    const emergencyBtn = document.getElementById('emergencyButton');
    const assistanceBtn = document.getElementById('assistanceButton');
    const foodBtn = document.getElementById('foodButton');
    const eventsBtn = document.getElementById('eventsButton');

    // Emergency button logic
    if (emergencyBtn) {
        emergencyBtn.onclick = async function() {
            const residentId = sessionStorage.getItem('resident_id');
            const payload = {
                alert_id: Math.floor(Math.random() * 1000000),
                resident_id: residentId,
                alert_type: "emergency",
                timestamp: new Date().toISOString(),
                details: "Emergency button pressed",
                status: "pending",
                unit: sessionStorage.getItem('unit')
            };
            try {
                await fetch('/api/alerts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                document.getElementById('emergencyModal').style.display = 'flex';
                document.getElementById('emergencyModalOkBtn').onclick = function() {
                    document.getElementById('emergencyModal').style.display = 'none';
                    window.location.href = '../html/residents_index.html';
                };
            } catch (err) {
                alert('Failed to send emergency alert.');
            }
        };
    }

    // Assistance button logic
    if (assistanceBtn) {
        assistanceBtn.onclick = function() {
            window.location.href = '../html/assistance.html';
        };
    }

    // Food button logic
    if (foodBtn) {
        foodBtn.onclick = function() {
            window.location.href = '../html/ondemand_food.html';
        };
    }

    // Events button logic
    if (eventsBtn) {
        eventsBtn.onclick = function() {
            window.location.href = '../html/events.html';
        };
    }
});


