// staticfiles/pedidos/js/pedido_form.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("pedido-form");
  if (!form) return;

  // 1) Cargar locale ES si existe
  if (window.flatpickr && flatpickr.l10ns && flatpickr.l10ns.es) {
    flatpickr.localize(flatpickr.l10ns.es);
  }

  // 2) Inicializar Flatpickr SIN altInput, mostrando dd/mm/YYYY
  ["fecha_inicio", "fecha_fin"].forEach((id) => {
    const el = document.getElementById(`id_${id}`);
    if (!el) return;
    flatpickr(el, {
      dateFormat: "d/m/Y", // formato que ve el usuario y se envía
      allowInput: true,
      wrap: false,
    });
  });

  // 3) Autofocus
  const first = form.querySelector(
    'input:not([type="hidden"]), select, textarea'
  );
  if (first) first.focus();

  // 4) Spinner al enviar
  form.addEventListener("submit", () => {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        Guardando…
      `;
    }
  });
  // === Servicios dinámicos ===
  document.addEventListener("DOMContentLoaded", () => {
    const cont = document.getElementById("servicios-container");
    const total = document.getElementById("id_serv-TOTAL_FORMS");
    const addBtn = document.getElementById("add-servicio");

    const template = (idx) => `
      <div class="card mb-3 p-3 position-relative">
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Excursión *</label>
            <input type="text" name="serv-${idx}-excursion" class="form-control">
          </div>
          <div class="col-md-2">
            <label class="form-label">Pax *</label>
            <input type="number" name="serv-${idx}-pax" class="form-control" min="1" value="1">
          </div>
          <div class="col-md-2">
            <label class="form-label">Emisores *</label>
            <input type="number" name="serv-${idx}-emisores" class="form-control" min="1" value="1">
          </div>
          <div class="col-md-4">
            <label class="form-label">Lugar entrega</label>
            <input type="text" name="serv-${idx}-lugar_entrega" class="form-control">
          </div>
        </div>
        <div class="mt-2">
          <label class="form-label">Bono</label>
          <input type="text" name="serv-${idx}-bono" class="form-control">
        </div>
        <input type="checkbox" hidden name="serv-${idx}-DELETE" id="id_serv-${idx}-DELETE">
        <button type="button" class="btn-close position-absolute top-0 end-0 eliminar-servicio"></button>
      </div>`;

    function addServicio() {
      const idx = parseInt(total.value, 10);
      cont.insertAdjacentHTML("beforeend", template(idx));
      total.value = idx + 1;
    }

    addBtn.addEventListener("click", addServicio);

    cont.addEventListener("click", (e) => {
      if (!e.target.classList.contains("eliminar-servicio")) return;
      const card = e.target.closest(".card");
      card.querySelector('[name$="-DELETE"]').checked = true;
      card.style.display = "none";
    });
  });
});
