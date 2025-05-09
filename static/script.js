// Add confirmation for admin deletion
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-admin');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to delete this admin?')) {
                e.preventDefault();
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("toggle-theme");
    const body = document.body;
  
    toggle.addEventListener("click", () => {
      body.classList.toggle("dark-mode");
    });
  });
  