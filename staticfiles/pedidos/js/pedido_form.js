// static/pedidos/js/pedido_form.js
document.addEventListener('DOMContentLoaded', () => {
  console.log('pedido_form.js cargado');  // ← confirma en consola

  const form = document.getElementById('pedido-form');
  if (!form) return;

  //
  // 1) Flatpickr en fechas
  //
  // (asume que Flatpickr y su locale ES ya se cargaron en base.html)
  ['fecha_inicio', 'fecha_fin'].forEach(id => {
    const el = document.getElementById(`id_${id}`);
    if (!el) return;
    flatpickr(el, {
      dateFormat: 'd/m/Y',
      allowInput: true
    });
  });

  //
  // 2) Autofocus en primer campo
  //
  const primer = form.querySelector('input:not([type=hidden]), select, textarea');
  if (primer) primer.focus();

  //
  // 3) Spinner y deshabilitar botón al enviar
  //
  form.addEventListener('submit', () => {
    const btn = form.querySelector('button[type=submit]');
    if (!btn) return;
    btn.disabled = true;
    btn.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      Guardando…
    `;
  });

  //
  // 4) Servicios dinámicos
  //
  const cont   = document.getElementById('servicios-container');
  const total  = document.getElementById('id_servicio-TOTAL_FORMS');
  const addBtn = document.getElementById('add-servicio');
  if (!cont || !total || !addBtn) return;

  const template = idx => `
    <div class="card mb-3 p-3 position-relative">
      <div class="row g-3">
        <div class="col-md-4">
          <label class="form-label">Excursión *</label>
          <input type="text" name="servicio-${idx}-excursion" class="form-control">
        </div>
        <div class="col-md-2">
          <label class="form-label">Pax *</label>
          <input type="number" name="servicio-${idx}-pax" class="form-control" min="1" value="1">
        </div>
        <div class="col-md-2">
          <label class="form-label">Emisores *</label>
          <input type="number" name="servicio-${idx}-emisores" class="form-control" min="1" value="1">
        </div>
        <div class="col-md-4">
          <label class="form-label">Lugar entrega</label>
          <input type="text" name="servicio-${idx}-lugar_entrega" class="form-control">
        </div>
      </div>
      <div class="mt-2">
        <label class="form-label">Bono</label>
        <input type="text" name="servicio-${idx}-bono" class="form-control">
      </div>
      <input type="checkbox" hidden name="servicio-${idx}-DELETE" id="id_servicio-${idx}-DELETE">
      <button type="button" class="btn-close eliminar-servicio position-absolute top-0 end-0"></button>
    </div>`;

  function addServicio() {
    const idx = parseInt(total.value, 10);
    cont.insertAdjacentHTML('beforeend', template(idx));
    total.value = idx + 1;
  }
  addBtn.addEventListener('click', addServicio);

  cont.addEventListener('click', e => {
    if (!e.target.classList.contains('eliminar-servicio')) return;
    const card = e.target.closest('.card');
    const del  = card.querySelector('[name$="-DELETE"]');
    if (del) del.checked = true;
    card.style.display = 'none';
  });
});
