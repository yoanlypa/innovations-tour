document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#form-pedido');
    if (!form) return;
  
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const resp = await fetch(form.action, {
        method: 'POST',
        body: data,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': data.get('csrfmiddlewaretoken'),
        }
      });
  
      if (resp.ok) {
        const json = await resp.json();
        if (json.success) {
          alert('✅ Pedido registrado satisfactoriamente.');
          window.location.href = json.redirect_url;
        } else {
          alert('❌ Hubo errores en el formulario. Revisa los campos.');
        }
      } else {
        alert('❌ Error inesperado al enviar el formulario.');
      }
    });
  });
  