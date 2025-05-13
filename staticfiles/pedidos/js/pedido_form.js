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
    
  // —— 1. Autofocus en primer campo —— 
  const firstInput = form.querySelector('input:not([type="hidden"]), select, textarea');
  if (firstInput) firstInput.focus();

  // —— 2. Spinner al enviar —— 
  form.addEventListener('submit', () => {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        Guardando…
      `;
    }
  });

  // —— 3. Dinámica de formulario de maletas —— 
  const cont = document.getElementById('maletas-container');
  const totalInp = document.getElementById('id_maleta-TOTAL_FORMS');
  const addBtn = document.getElementById('add-maleta');
  const prefix = 'maleta';

  // HTML plantilla para nueva maleta
  const templateHTML = idx => `
    <div class="card mb-3 p-3 position-relative">
      <button type="button" class="btn-close position-absolute top-0 end-0 eliminar-maleta"
              aria-label="Eliminar maleta"></button>
      <div class="row g-3">
        <div class="col-md-6">
          <label for="id_${prefix}-${idx}-guia" class="form-label">
            Guía <span class="text-danger">*</span>
          </label>
          <input type="text"
                 name="${prefix}-${idx}-guia"
                 id="id_${prefix}-${idx}-guia"
                 class="form-control">
        </div>
        <div class="col-md-6">
          <label for="id_${prefix}-${idx}-cantidad_pax" class="form-label">
            Cantidad de Pax <span class="text-danger">*</span>
          </label>
          <input type="number"
                 name="${prefix}-${idx}-cantidad_pax"
                 id="id_${prefix}-${idx}-cantidad_pax"
                 class="form-control"
                 min="1"
                 value="1">
        </div>
      </div>
      <input type="checkbox"
             name="${prefix}-${idx}-DELETE"
             id="id_${prefix}-${idx}-DELETE"
             hidden>
    </div>`;

  // Añade la primera maleta si no hay ninguna
  if (parseInt(totalInp.value, 10) === 0) {
    cont.insertAdjacentHTML('beforeend', templateHTML(0));
    totalInp.value = 1;
  }

  // Click en “Añadir maleta”
  addBtn.addEventListener('click', () => {
    const idx = parseInt(totalInp.value, 10);
    cont.insertAdjacentHTML('beforeend', templateHTML(idx));
    totalInp.value = idx + 1;
  });

  // Botón para eliminar maleta
  cont.addEventListener('click', e => {
    if (!e.target.classList.contains('eliminar-maleta')) return;
    const box = e.target.closest('.card');
    const del = box.querySelector('input[type="checkbox"]');
    del.checked = true;
    box.remove();  // quitamos del DOM
  });
});
  