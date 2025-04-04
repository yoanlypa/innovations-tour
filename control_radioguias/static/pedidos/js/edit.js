// ✅ Manejo de la tabla de pedidos
// Este script maneja la interacción con la tabla de pedidos, incluyendo la edición, eliminación y duplicación de pedidos.  
// También maneja la actualización de checkboxes sin recargar la página.
// Se utiliza Bootstrap para los modales y AJAX para la actualización de datos.
// Se asume que el HTML tiene una estructura específica para los modales y la tabla de pedidos.
// Se utiliza el método fetch para realizar solicitudes AJAX y se maneja la respuesta en formato JSON.
// Se utiliza el método getCookie para obtener la cookie CSRF necesaria para las solicitudes POST.
// Se utiliza el método closest para encontrar el elemento padre más cercano que coincida con un selector específico.
// Se utiliza el método querySelector para seleccionar elementos del DOM y se utilizan eventos para manejar la interacción del usuario.
// Se utiliza el método addEventListener para agregar eventos a los elementos seleccionados.
// Se utiliza el método matches para verificar si un elemento coincide con un selector específico.
// Se utiliza el método setAttribute para establecer atributos en los elementos seleccionados.
// Se utiliza el método getAttribute para obtener atributos de los elementos seleccionados.
// Se utiliza el método preventDefault para evitar el comportamiento predeterminado de un evento.
// Se utiliza el método stopPropagation para detener la propagación de un evento en la cadena de eventos.
// Se utiliza el método alert para mostrar mensajes al usuario en caso de error o éxito.
// Se utiliza el método console.error para mostrar errores en la consola del navegador.
// Se utiliza el método console.log para mostrar mensajes en la consola del navegador para depuración.
// Se utiliza el método bootstrap.Modal para crear y mostrar modales de Bootstrap.
// Se utiliza el método bootstrap.Modal.getInstance para obtener una instancia de un modal de Bootstrap.
// Se utiliza el método bootstrap.Modal.hide para ocultar un modal de Bootstrap.
// Se utiliza el método bootstrap.Modal.show para mostrar un modal de Bootstrap.
// Se utiliza el método bootstrap.Modal.dispose para eliminar un modal de Bootstrap.
// Se utiliza el método bootstrap.Modal.getOrCreateInstance para obtener o crear una instancia de un modal de Bootstrap.

  

document.addEventListener("DOMContentLoaded", function() {
    // Función para obtener la cookie CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
  
    // ✅ Actualizar checkboxes sin recargar la página
    document.querySelector('.table-responsive').addEventListener('change', function(e) {
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
  
    // ✅ Manejo del botón "Editar"
    document.querySelector('.table-responsive').addEventListener('click', function(e) {
        if (e.target && e.target.matches('.btn-editar')) {
            const btn = e.target;
            const row = btn.closest('tr');
            const id = row.getAttribute('data-id');
            const eCheckbox = row.querySelector('.campo-e input');
            const rCheckbox = row.querySelector('.campo-r input');
  
            // Cargar datos en el modal de edición
            document.getElementById('editarE').checked = eCheckbox.checked;
            document.getElementById('editarR').checked = rCheckbox.checked;
            document.getElementById('formEditarER').action = `/pedidos/editar_stock/${id}/`;
  
            const modal = new bootstrap.Modal(document.getElementById('editarERModal'));
            modal.show();
        }
    });
  
    // ✅ Manejo del botón "Duplicar"
    document.querySelector('.table-responsive').addEventListener('click', function(e) {
        if (e.target && e.target.matches('.btn-duplicar')) {
            const btn = e.target;
            const row = btn.closest('tr');
            const id = row.getAttribute('data-id');
  
            // Aquí puedes agregar más datos si necesitas duplicar más campos
            document.getElementById('duplicarPedidoID').value = id;
  
            const modal = new bootstrap.Modal(document.getElementById('duplicarModal'));
            modal.show();
        }
    });
  });
  
  // ✅ Manejo del botón "Eliminar"
  document.querySelector('.table-responsive').addEventListener('click', function(e) {
    if (e.target && e.target.matches('.btn-eliminar')) {
        const btn = e.target;
        const row = btn.closest('tr');
        const id = row.getAttribute('data-id');
  
        // Cargar ID en el modal de eliminación
        document.getElementById('eliminarPedidoID').value = id;
  
        const modal = new bootstrap.Modal(document.getElementById('eliminarModal'));
        modal.show();
    }
  });
  