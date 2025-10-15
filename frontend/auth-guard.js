// This script runs on every page except the login page.
// It checks if the user is authenticated. If not, it shows an alert and redirects.

(function() {
    // Check for the 'isLoggedIn' flag in session storage
    const isLoggedIn = sessionStorage.getItem('isLoggedIn');

    // If the flag is not 'true', show an alert and then redirect
    if (isLoggedIn !== 'true') {
        alert('You must be logged in to view this page.');
        // We use replace() so the user cannot use the "back" button to access a protected page
        window.location.replace('./login.html');
    }

    // --- Logout Functionality ---
    // This part adds the logout logic to the logout button on each page
    document.addEventListener('DOMContentLoaded', function() {
        // Find the logout button by its text content
        const logoutButton = Array.from(document.querySelectorAll('.btn')).find(el => el.textContent.trim().includes('Logout'));
        
        if (logoutButton) {
            logoutButton.addEventListener('click', function(event) {
                event.preventDefault();
                // Clear the session storage
                sessionStorage.removeItem('isLoggedIn');
                // Redirect to the login page
                window.location.href = './login.html';
            });
        }
    });
})();

