document.addEventListener('DOMContentLoaded', () => {
    // Replace with your actual backend API endpoint
    const apiUrl = 'http://localhost:5000/api/doctor/input';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            // Assuming the backend returns { input: "some value" }
            const inputElement = document.getElementById('doctor-input');
            if (inputElement && data.input) {
                inputElement.textContent = data.input;
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
});