function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(cookie => {
        const [key, val] = cookie.trim().split('=');
        if (key === name) cookieValue = decodeURIComponent(val);
      });
    }
    return cookieValue;
  }
  
  const csrftoken = getCookie('csrftoken');

  // 1. Actualizar checkboxes E y R vía AJAX
  const tableContainer = document.querySelector('.table-responsive');
  if (tableContainer) {
      tableContainer.addEventListener('change', function(e) {
          if (e.target && e.target.matches('.checklist')) {
              const checkbox = e.target;
              const row = checkbox.closest('tr');
              const id = row.getAttribute('data-id');
              const field = checkbox.getAttribute('data-field');
              const value = checkbox.checked;

              fetch('/pedidos/ajax_update_checklist/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/x-www-form-urlencoded',
                      'X-CSRFToken': getCookie('csrftoken')
                  },
                  body: `id=${id}&field=${field}&value=${value}`
              })
              .then(response => response.json())
              .then(data => {
                  if (!data.success) {
                      alert('Error al actualizar: ' + data.error);
                  }
              })
              .catch(err => {
                  console.error('Error en AJAX:', err);
              });
          }
      });

      // 2. Manejo del botón "Editar": Abrir modal de edición con todos los datos
      tableContainer.addEventListener('click', function(e) {
          if (e.target && e.target.matches('.btn-editar')) {
              const btn = e.target;
              const row = btn.closest('tr');
              const id = row.getAttribute('data-id');

              // Extraer datos de la fila
              const pax = row.querySelector('.campo-pax').innerText.trim();
              const lugar = row.querySelector('.campo-lugar').innerText.trim();
              const excursion = row.querySelector('.campo-excursion').innerText.trim();
              const guia = row.querySelector('.campo-guia').innerText.trim();
              const fecha = row.querySelector('.campo-fecha').innerText.trim();
              const entregado = row.querySelector('.campo-e input').checked;
              const recogido = row.querySelector('.campo-r input').checked;

              // Rellenar los campos del modal de edición
              document.getElementById('editarPax').value = pax;
              document.getElementById('editarLugar').value = lugar;
              document.getElementById('editarExcursion').value = excursion;
              document.getElementById('editarGuia').value = guia;
              document.getElementById('editarFecha').value = fecha;
              document.getElementById('editarE').checked = entregado;
              document.getElementById('editarR').checked = recogido;

              // Establecer la acción del formulario de edición (por ejemplo, la URL para actualizar)
              document.getElementById('formEditar').action = `/pedidos/editar_stock/${id}/`;

              // Mostrar el modal de edición
              const modalEditar = new bootstrap.Modal(document.getElementById('editarModal'));
              modalEditar.show();
          }
      });

      // 3. Manejo del botón "Duplicar": Abrir modal de nuevo registro prellenado
      tableContainer.addEventListener('click', function(e) {
          if (e.target && e.target.matches('.btn-duplicar')) {
              const btn = e.target;
              const row = btn.closest('tr');
              // Extraer datos de la fila
              const pax = row.querySelector('.campo-pax').innerText.trim();
              const lugar = row.querySelector('.campo-lugar').innerText.trim();
              const excursion = row.querySelector('.campo-excursion').innerText.trim();
              const guia = row.querySelector('.campo-guia').innerText.trim();
              const fecha = row.querySelector('.campo-fecha').innerText.trim();
              const entregado = row.querySelector('.campo-e input').checked;
              const recogido = row.querySelector('.campo-r input').checked;
            // Manejo del botón "Eliminar"
      tableContainer.addEventListener('click', function(e) {
          if (e.target && e.target.matches('.btn-eliminar')) {
              const btn = e.target;
              const row = btn.closest('tr');
              const id = row.getAttribute('data-id');
              
              // Confirmar la acción de eliminación
              if (!confirm('¿Estás seguro de eliminar este registro?')) {
                  return;
              }
              
              // Enviar la petición AJAX para eliminar el registro
              fetch(`/pedidos/eliminar_stock/${id}/`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/x-www-form-urlencoded',
                      'X-CSRFToken': getCookie('csrftoken')
                  },
                  body: `id=${id}`
              })
              .then(response => response.json())
              .then(data => {
                  if (data.success) {
                      // Eliminar la fila de la tabla si se eliminó correctamente
                      row.remove();
                  } else {
                      alert('Error al eliminar: ' + data.error);
                  }
              })
              .catch(err => {
                  console.error('Error en AJAX al eliminar:', err);
              });
          }
        });

              // Rellenar los campos del modal de nuevo registro
              document.getElementById('nuevoPax').value = pax;
              document.getElementById('nuevoLugar').value = lugar;
              document.getElementById('nuevaExcursion').value = excursion;
              document.getElementById('nuevoGuia').value = guia;
              document.getElementById('nuevaFecha').value = fecha;
              document.getElementById('nuevoEntregado').checked = entregado;
              document.getElementById('nuevoRecogido').checked = recogido;

              // Mostrar el modal de nuevo registro
              const modalNuevo = new bootstrap.Modal(document.getElementById('nuevoRegistroModal'));
              modalNuevo.show();
          }
      });
  } else {
      console.error("No se encontró el contenedor '.table-responsive'");
  }
