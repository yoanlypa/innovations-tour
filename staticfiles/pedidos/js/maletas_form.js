document.addEventListener('DOMContentLoaded', () => {
    const addMaletaBtn = document.getElementById('add-maleta');
    const maletasContainer = document.getElementById('maletas-container');
    const totalFormsInput = document.getElementById('id_form-TOTAL_FORMS');
  
    if (!addMaletaBtn || !maletasContainer || !totalFormsInput) return;
  
    addMaletaBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const totalForms = parseInt(totalFormsInput.value, 10);
  
      // Clonar la primera maleta como plantilla
      const firstForm = maletasContainer.querySelector('.maleta-form');
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
      maletasContainer.appendChild(newForm);
  
      // Actualizar el TOTAL_FORMS
      totalFormsInput.value = totalForms + 1;
    });
  });
  