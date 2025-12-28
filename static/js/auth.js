// For register.html
const registerForm = document.getElementById('register-form');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
        };
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (response.ok) {
            localStorage.setItem('access', result.access);
            localStorage.setItem('refresh', result.refresh);
            alert('Registered! Tokens stored in localStorage.');
            // Redirect to e-commerce home or login
        } else {
            alert('Error: ' + JSON.stringify(result));
        }
    });
}

// For login.html
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
        };
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (response.ok) {
            localStorage.setItem('access', result.access);
            localStorage.setItem('refresh', result.refresh);
            alert('Logged in! Tokens stored in localStorage.');
            // Use access token for protected e-commerce APIs
        } else {
            alert('Error: ' + JSON.stringify(result));
        }
    });
}

// Refresh token example (call when access expires)
async function refreshToken() {
    const refresh = localStorage.getItem('refresh');
    if (refresh) {
        const response = await fetch('/api/token/refresh/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh }),
        });
        const result = await response.json();
        if (response.ok) {
            localStorage.setItem('access', result.access);
        }
    }
}