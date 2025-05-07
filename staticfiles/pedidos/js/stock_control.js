$(document).ready(function () {
    const $modal = $('#nuevoRegistroModal');
    const $form = $modal.find('form');
  
    // Agrega una maleta al formset
    $('#add-maleta').click(function (e) {
      e.preventDefault();
      const $container = $('#maletas-container');
      const totalForms = $('#id_form-TOTAL_FORMS');
      const formIdx = parseInt(totalForms.val());
  
      const $newForm = $container.find('.maleta-form').first().clone(true);
      $newForm.find('input, select, textarea').each(function () {
        const name = $(this).attr('name').replace(/-\d+-/, `-${formIdx}-`);
        const id = 'id_' + name;
        $(this).attr({ name, id }).val('');
      });
      $newForm.find('input[type="checkbox"]').prop('checked', false);
      $container.append($newForm);
      totalForms.val(formIdx + 1);
    });
  
    // Envío del formulario vía AJAX
    $form.on('submit', function (e) {
      e.preventDefault();
      const formData = new FormData(this);
  
      $.ajax({
        url: $form.attr('action'),
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
          'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
        },
        success: function (response) {
          if (response.success) {
            window.location.href = '/pedidos/stock/';
          } else {
            alert('Error al guardar. Verifica los campos.');
            console.error('Errores:', response.errors, response.formset_errors);
          }
        },
        error: function (xhr) {
          alert('Error de red o de validación.');
          console.error(xhr.responseText);
        }
      });
    });
  
    // Precargar datos del pedido seleccionado
    $('#id_pedido').change(function () {
      const pedidoId = $(this).val();
      if (!pedidoId) return;
  
      $.getJSON('/pedidos/stock/cargar_datos_pedido/', { pedido_id: pedidoId }, function (data) {
        $('#id_excursion').val(data.excursion);
        $('#id_empresa').val(data.empresa);
        $('#id_lugar_entrega').val(data.lugar_entrega);
        $('#id_lugar_recogida').val(data.lugar_recogida);
        $('#id_guia').val(data.guia);
        $('#id_fecha_inicio').val(data.fecha_inicio);
        $('#id_fecha_fin').val(data.fecha_fin);
        $('#id_notas').val(data.notas);
  
        const $container = $('#maletas-container');
        $container.empty();
        const totalForms = $('#id_form-TOTAL_FORMS');
  
        data.maletas.forEach((m, idx) => {
          const $formHtml = $(`
            <div class="maleta-form">
              <label for="id_form-${idx}-guia">Guía</label>
              <input type="text" name="form-${idx}-guia" id="id_form-${idx}-guia" value="${m.guia}" required>
              <label for="id_form-${idx}-cantidad_pax">Pax</label>
              <input type="number" name="form-${idx}-cantidad_pax" id="id_form-${idx}-cantidad_pax" value="${m.pax}" required>
            </div>`);
          $container.append($formHtml);
        });
        totalForms.val(data.maletas.length);
      });
    });
  });