// staticfiles/pedidos/js/pedido_form.js

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('pedido-form');
  if (!form) return;

  // —— 0. Scroll a primer error si lo hay —— 
  const firstError = document.querySelector('.invalid-feedback, .alert-danger');
  if (firstError) {
    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // —— 1. Flatpickr en campos de fecha —— 
  if (window.flatpickr) {
    flatpickr("#id_fecha_inicio", {
      locale: "es",
      dateFormat: "d/m/Y",
      allowInput: true,
      altInput: true,
      altFormat: "d/m/Y",
      ariaDateFormat: "Y-m-d"
    });
    flatpickr("#id_fecha_fin", {
      locale: "es",
      dateFormat: "d/m/Y",
      allowInput: true,
      altInput: true,
      altFormat: "d/m/Y",
      ariaDateFormat: "Y-m-d"
    });
  }

  // —— 2. Autofocus en primer campo —— 
  const firstInput = form.querySelector('input:not([type="hidden"]), select, textarea');
  if (firstInput) firstInput.focus();

  // —— 3. Spinner al enviar —— 
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

  // —— 4. Dinámica de maletas —— 
  // 4.1. Buscar el input de TOTAL_FORMS
  const totalInp = form.querySelector('input[name$="-TOTAL_FORMS"]');
  const cont = document.getElementById('maletas-container');
  const addBtn = document.getElementById('add-maleta');

  if (!totalInp || !cont || !addBtn) {
    console.warn('Formset de maletas no se encontró correctamente.');
    return;
  }

  // 4.2. Derivar automáticamente el prefix: todo antes de "-TOTAL_FORMS"
  const prefix = totalInp.name.replace('-TOTAL_FORMS', '');

  // 4.3. Plantilla para nueva maleta
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

  // 4.4. Si no hay maletas al inicio, añadir una
  if (parseInt(totalInp.value, 10) === 0) {
    cont.insertAdjacentHTML('beforeend', templateHTML(0));
    totalInp.value = 1;
  }

  // 4.5. Al hacer clic en “Añadir maleta”
  addBtn.addEventListener('click', () => {
    const idx = parseInt(totalInp.value, 10);
    cont.insertAdjacentHTML('beforeend', templateHTML(idx));
    totalInp.value = idx + 1;
  });

  // 4.6. Manejar eliminación de maleta
  cont.addEventListener('click', e => {
    if (!e.target.classList.contains('eliminar-maleta')) return;
    const box = e.target.closest('.card');
    const del = box.querySelector('input[type="checkbox"]');
    if (del) del.checked = true;
    box.remove();
  });
});
