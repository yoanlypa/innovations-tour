// staticfiles/pedidos/js/pedido_form.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('pedido-form');
  if (!form) return;

  // Flatpickr
  if (window.flatpickr) {
    ["fecha_inicio","fecha_fin"].forEach(id=>{
      const sel = document.getElementById(`id_${id}`);
      if (sel) flatpickr(sel, {
        locale: "es",
        dateFormat: "d/m/Y",
        allowInput: true,
        altInput: true,
        altFormat: "d/m/Y",
      });
    });
  }

  // Autofocus
  const first = form.querySelector('input:not([type="hidden"]), select, textarea');
  if (first) first.focus();

  // Spinner al enviar
  form.addEventListener('submit', () => {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"
                        aria-hidden="true"></span> Guardando…`;
    }
  });

  // Dinámica de maletas (solo 1 listener)
  const totalInp = form.querySelector('input[name$="-TOTAL_FORMS"]');
  const cont     = document.getElementById('maletas-container');
  const addBtn   = document.getElementById('add-maleta');
  if (!totalInp || !cont || !addBtn) return;

  const pr = totalInp.name.replace('-TOTAL_FORMS','');
  const tpl = idx => `
    <div class="card mb-3 p-3 position-relative">
      <button type="button" class="btn-close position-absolute top-0 end-0 eliminar-maleta"></button>
      <div class="row g-3">
        <div class="col-md-6">
          <label for="id_${pr}-${idx}-guia" class="form-label">Guía *</label>
          <input type="text" name="${pr}-${idx}-guia" id="id_${pr}-${idx}-guia"
                 class="form-control">
        </div>
        <div class="col-md-6">
          <label for="id_${pr}-${idx}-cantidad_pax" class="form-label">Cantidad de Pax *</label>
          <input type="number" name="${pr}-${idx}-cantidad_pax" id="id_${pr}-${idx}-cantidad_pax"
                 class="form-control" min="1" value="1">
        </div>
      </div>
      <input type="checkbox" name="${pr}-${idx}-DELETE" id="id_${pr}-${idx}-DELETE" hidden>
    </div>`;

  // Si TOTAL_FORMS=0, solo entonces metemos 1 inicial. Si no, dejamos las que Django ya puso.
  if (+totalInp.value === 0) {
    cont.insertAdjacentHTML('beforeend', tpl(0));
    totalInp.value = 1;
  }

  addBtn.onclick = () => {
    const idx = +totalInp.value;
    cont.insertAdjacentHTML('beforeend', tpl(idx));
    totalInp.value = idx + 1;
  };

  cont.onclick = e => {
    if (!e.target.classList.contains('eliminar-maleta')) return;
    const card = e.target.closest('.card');
    const cb   = card.querySelector('input[type="checkbox"]');
    if (cb) cb.checked = true;
    card.remove();
  };
});
