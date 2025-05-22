document.addEventListener('DOMContentLoaded', () => {
    const addServicioBtn = document.getElementById('add-servicio');
    const serviciosContainer = document.getElementById('servicios-container');
    const totalFormsInput = document.getElementById('id_servicio-TOTAL_FORMS');
  
    if (!addServicioBtn || !serviciosContainer || !totalFormsInput) return;
  
    addServicioBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const totalForms = parseInt(totalFormsInput.value, 10);
  
      // Clonar el primer servicio como plantilla
      const firstForm = serviciosContainer.querySelector('.servicio-form');
      if (!firstForm) return;
  
      const newForm = firstForm.cloneNode(true);
  
      // Limpiar los valores del nuevo formulario
      newForm.querySelectorAll('input, select, textarea').forEach(input => {
        if (input.type === 'checkbox' || input.type === 'radio') {
          input.checked = false;
        } else {
          input.value = '';
        }
  
        // Reemplazar los índices de nombres y IDs
        if (input.name) {
          input.name = input.name.replace(/form-\d+-/, `form-${totalForms}-`);
        }
        if (input.id) {
          input.id = input.id.replace(/form-\d+-/, `form-${totalForms}-`);
        }
      });
  
      // Agregar el nuevo formulario
      serviciosContainer.appendChild(newForm);
  
      // Actualizar el TOTAL_FORMS
      totalFormsInput.value = totalForms + 1;
    });
  });
  