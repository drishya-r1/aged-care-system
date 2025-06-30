
// Assumes ?username=... in URL
function getQueryParam(name) {
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
}
const username = getQueryParam('username');
if (username) {
    fetch(`/residents/${username}`)
        .then(res => res.json())
        .then(data => {
            const profileDiv = document.getElementById('profile');
            if (data.success) {
                const user = data.profile;
                profileDiv.innerHTML = Object.entries(user).map(
                    ([k, v]) => `<div class="profile-field"><span class="profile-label">${k.replace(/_/g, ' ')}:</span> ${v ?? ''}</div>`
                ).join('');
            } else {
                profileDiv.textContent = data.message;
            }
        });
} else {
    document.getElementById('profile').textContent = "No username specified.";
}