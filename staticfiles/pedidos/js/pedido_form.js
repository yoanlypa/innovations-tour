// staticfiles/pedidos/js/pedido_form.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('pedido-form');
  if (!form) return;

  // 1) Localizar Flatpickr en español
  if (window.flatpickr && flatpickr.l10ns && flatpickr.l10ns.es) {
    flatpickr.localize(flatpickr.l10ns.es);
  }

  // 2) Inicializar Flatpickr: value=ISO, visible=dd/mm/YYYY
  ["fecha_inicio", "fecha_fin"].forEach(id => {
    const el = document.getElementById(`id_${id}`);
    if (el) {
      flatpickr(el, {
        dateFormat: "Y-m-d",      // formato que se envía al servidor
        altInput: true,           // elemento visible aparte
        altFormat: "d/m/Y",       // formato que ve el usuario
        allowInput: true
      });
    }
  });

  // 3) Autofocus en primer campo
  const first = form.querySelector('input:not([type="hidden"]), select, textarea');
  if (first) first.focus();

  // 4) Spinner al enviar
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

  // 5) Dinámica de maletas
  const totalInp = form.querySelector('input[name$="-TOTAL_FORMS"]');
  const cont     = document.getElementById('maletas-container');
  const addBtn   = document.getElementById('add-maleta');
  if (!totalInp || !cont || !addBtn) return;

  const prefix = totalInp.name.replace('-TOTAL_FORMS', '');
  const plantilla = idx => `
    <div class="card mb-3 p-3 position-relative">
      <button type="button" class="btn-close position-absolute top-0 end-0 eliminar-maleta"></button>
      <div class="row g-3">
        <div class="col-md-6">
          <label for="id_${prefix}-${idx}-guia" class="form-label">Guía *</label>
          <input type="text" name="${prefix}-${idx}-guia" id="id_${prefix}-${idx}-guia"
                 class="form-control">
        </div>
        <div class="col-md-6">
          <label for="id_${prefix}-${idx}-cantidad_pax" class="form-label">Cantidad de Pax *</label>
          <input type="number" name="${prefix}-${idx}-cantidad_pax" id="id_${prefix}-${idx}-cantidad_pax"
                 class="form-control" min="1" value="1">
        </div>
      </div>
      <input type="checkbox" name="${prefix}-${idx}-DELETE" id="id_${prefix}-${idx}-DELETE" hidden>
    </div>`;

  // Añadir la primera maleta si TOTAL_FORMS=0
  if (parseInt(totalInp.value, 10) === 0) {
    cont.insertAdjacentHTML('beforeend', plantilla(0));
    totalInp.value = 1;
  }

  // Añadir nuevas maletas
  addBtn.onclick = () => {
    const idx = parseInt(totalInp.value, 10);
    cont.insertAdjacentHTML('beforeend', plantilla(idx));
    totalInp.value = idx + 1;
  };

  // Eliminar maleta
  cont.onclick = e => {
    if (!e.target.classList.contains('eliminar-maleta')) return;
    const card = e.target.closest('.card');
    const cb = card.querySelector('input[type="checkbox"]');
    if (cb) cb.checked = true;
    card.remove();
  };
});
