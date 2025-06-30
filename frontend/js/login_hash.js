// login_hash.js: Hash password before sending to backend
async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await window.crypto.subtle.digest('SHA-256', data);
    return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.onsubmit = async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const hashedPassword = await hashPassword(password);
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', hashedPassword);
            const response = await fetch('/login', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                const data = await response.json();
                sessionStorage.setItem('username', data.user.username);
                sessionStorage.setItem('userid', data.user.userid);
                if (data.user && data.user.usertype === "RES") {
                    window.location.href = '../frontend/html/residents_index.html';
                } else if (data.user && data.user.usertype === "NUR") {
                    window.location.href = '../frontend/html/nurseportaltwo.html';
                } else if (data.user.usertype === 'ADM') {
                    window.location.href = '../frontend/html/admin.html';
                } else {
                    alert('Unknown user type');
                }
            } else {
                alert('Login failed');
            }
        };
    }
});
