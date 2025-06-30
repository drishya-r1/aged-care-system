document.getElementById('onboardForm').onsubmit = async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = Object.fromEntries(new FormData(form).entries());
    try {
        const res = await fetch('/residents/new', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await res.json();
        const msg = document.getElementById('msg');
        msg.textContent = result.message;
        msg.style.color = result.success ? 'green' : 'red';
        if(result.success) form.reset();
    } catch (error) {
        const msg = document.getElementById('msg');
        msg.textContent = "Failed to connect to server.";
        msg.style.color = 'red';
        console.error('Error:', error);
    }
};
document.getElementById('onboardForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    fetch('/residents/new', {
        method: 'POST',
        body: data
    })
    .then(response => response.json())
    .then(result => {
        const msg = document.getElementById('msg');
        msg.textContent = result.message;
        msg.style.color = result.success ? 'green' : 'red';
        if(result.success) form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
