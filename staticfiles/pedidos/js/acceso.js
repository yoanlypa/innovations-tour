// staticfiles/pedidos/js/acceso.js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = document.querySelector(btn.getAttribute('data-target'));
      if (!input) return;
      const icon = btn.querySelector('i');
      if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('bi-eye-slash', 'bi-eye');
      } else {
        input.type = 'password';
        icon.classList.replace('bi-eye', 'bi-eye-slash');
      }
    });
  });
});
