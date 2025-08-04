// En tu JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.selector-graficas button');
    buttons.forEach(btn => {
      btn.addEventListener('click', function() {
        buttons.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
      });
    });

  // Provincias y comunidades autonomas
  // --- Multi-select Comunidades ---
  const comMulti = document.getElementById('comunidades-multiselect');
  const comHeader = document.getElementById('com-header');
  const comOptions = document.getElementById('com-options');
  const comPills = document.getElementById('com-pills');
  const comCheckboxes = comOptions.querySelectorAll('input[type="checkbox"]');

  // --- Multi-select Provincias ---
  const provMulti = document.getElementById('provincias-multiselect');
  const provHeader = document.getElementById('prov-header');
  const provOptions = document.getElementById('prov-options');
  const provPills = document.getElementById('prov-pills');
  const provCheckboxes = provOptions.querySelectorAll('input[type="checkbox"]');

  // Mostrar/ocultar opciones al pulsar header
  comHeader.addEventListener('click', function(e) {
    comMulti.classList.toggle('open');
  });
  provHeader.addEventListener('click', function(e) {
    provMulti.classList.toggle('open');
  });

  // Cerrar si se hace click fuera
  document.addEventListener('click', function(e) {
    if (!comMulti.contains(e.target)) comMulti.classList.remove('open');
    if (!provMulti.contains(e.target)) provMulti.classList.remove('open');
  });

  // Actualizar pills y header para comunidades
  function updateComPills() {
    comPills.innerHTML = '';
    let selected = [];
    comCheckboxes.forEach(cb => {
      if (cb.checked) {
        selected.push(cb.parentElement.textContent.trim());
        const pill = document.createElement('span');
        pill.className = 'pill';
        pill.textContent = cb.parentElement.textContent.trim();
        const remove = document.createElement('span');
        remove.className = 'pill-remove';
        remove.textContent = '×';
        remove.onclick = () => {
          cb.checked = false;
          updateComPills();
          exclusividad();
        };
        pill.appendChild(remove);
        comPills.appendChild(pill);
      }
    });
    comHeader.textContent = selected.length > 0 ? `${selected.length} seleccionadas` : 'Selecciona comunidades';
  }

  // Actualizar pills y header para provincias
  function updateProvPills() {
    provPills.innerHTML = '';
    let selected = [];
    provCheckboxes.forEach(cb => {
      if (cb.checked) {
        selected.push(cb.parentElement.textContent.trim());
        const pill = document.createElement('span');
        pill.className = 'pill';
        pill.textContent = cb.parentElement.textContent.trim();
        const remove = document.createElement('span');
        remove.className = 'pill-remove';
        remove.textContent = '×';
        remove.onclick = () => {
          cb.checked = false;
          updateProvPills();
          exclusividad();
        };
        pill.appendChild(remove);
        provPills.appendChild(pill);
      }
    });
    provHeader.textContent = selected.length > 0 ? `${selected.length} seleccionadas` : 'Selecciona provincias';
  }

  // Exclusividad: si hay alguna comunidad seleccionada, desactiva provincias y viceversa
  function exclusividad() {
    const comunidadesMarcadas = [...comCheckboxes].some(cb => cb.checked);
    const provinciasMarcadas = [...provCheckboxes].some(cb => cb.checked);

    if (comunidadesMarcadas) {
      provCheckboxes.forEach(cb => { cb.checked = false; cb.disabled = true; });
      updateProvPills();
      provHeader.classList.add('disabled');
    } else {
      provCheckboxes.forEach(cb => { cb.disabled = false; });
      provHeader.classList.remove('disabled');
    }

    if (provinciasMarcadas) {
      comCheckboxes.forEach(cb => { cb.checked = false; cb.disabled = true; });
      updateComPills();
      comHeader.classList.add('disabled');
    } else {
      comCheckboxes.forEach(cb => { cb.disabled = false; });
      comHeader.classList.remove('disabled');
    }
  }

  comCheckboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      updateComPills();
      exclusividad();
    });
  });

  provCheckboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      updateProvPills();
      exclusividad();
    });
  });

  // Inicializar
  updateComPills();
  updateProvPills();
  
  // Función para verificar selecciones
  function verificarSelecciones() {
    // Verificar si hay comunidades seleccionadas
    const hayComunidades = comPills && comPills.children.length > 0;
    
    // Verificar si hay provincias seleccionadas
    const hayProvincias = document.querySelector('.pill') && 
                          provOptions && 
                          provOptions.querySelectorAll('input:checked').length > 0;
    
    // Deshabilitar por completo la apertura del desplegable de provincias
    if (hayComunidades) {
      provHeader.style.pointerEvents = 'none';
      provHeader.classList.add('disabled');
    } else {
      provHeader.style.pointerEvents = 'auto';
      provHeader.classList.remove('disabled');
    }
    
    // Deshabilitar por completo la apertura del desplegable de comunidades
    if (hayProvincias) {
      comHeader.style.pointerEvents = 'none';
      comHeader.classList.add('disabled');
    } else {
      comHeader.style.pointerEvents = 'auto';
      comHeader.classList.remove('disabled');
    }
  }
  
  // Verificar al cargar la página
  verificarSelecciones();
  
  // Verificar después de cambios en los checkboxes
  document.querySelectorAll('.multi-select input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', verificarSelecciones);
  });
  
  // Observar cambios en los pills
  const observer = new MutationObserver(verificarSelecciones);
  if (comPills) observer.observe(comPills, { childList: true });
  if (provPills) observer.observe(provPills, { childList: true });

  window.addEventListener('click', function(e) {
  const dropdownContent = document.querySelector('.dropdown-content');
  if (!e.target.matches('.dropdown-btn')) {
    if (dropdownContent) {
      dropdownContent.style.display = 'none';
    }
  }
});

  // Control del rango de años
  const rangoCheck = document.getElementById('rango');
  const rangoInput = document.getElementById('rango-anios');
  
  rangoCheck.addEventListener('change', function() {
    rangoInput.disabled = !this.checked;
    document.getElementById('anio').disabled = this.checked;
  });

  if (rangoInput) {
    rangoInput.addEventListener('input', function(e) {
      // Solo permite números y guion
      this.value = this.value.replace(/[^0-9\-]/g, '');
    });
    // Opcional: prevenir pegar texto no válido
    rangoInput.addEventListener('paste', function(e) {
      const pasted = (e.clipboardData || window.clipboardData).getData('text');
      if (!/^[0-9\-]*$/.test(pasted)) {
        e.preventDefault();
      }
    });
  }

  // Control de los checkboxes de provincias
  const provinciaCheckboxes = document.querySelectorAll('input[name="provincia"]');
  provinciaCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      if(this.checked) {
        // Lógica para deseleccionar otros filtros si es necesario
      }
    });
  });

  // Generar gráfica
  document.querySelector('.btn-generar').addEventListener('click', function() {
    // Recoge provincias y comunidades seleccionadas
    const provincias = Array.from(document.querySelectorAll('#prov-options input[type="checkbox"]:checked')).map(cb => cb.value);
    const comunidades = Array.from(document.querySelectorAll('#com-options input[type="checkbox"]:checked')).map(cb => cb.value);

    // Recoge año y rango
    const anio = document.getElementById('anio').value;
    const rangoCheck = document.getElementById('rango');
    const rangoAnios = document.getElementById('rango-anios').value;

    // Recoge filtros extra
    const mostrarGenero = document.getElementById('filtro-genero').checked;
    const mostrarMortalidad = document.getElementById('filtro-mortalidad').checked;

    // Validación básica en frontend
    if ((provincias.length === 0 && comunidades.length === 0) || (anio.length === 0 && rangoAnios === 0)) {
        alert('Debes seleccionar al menos una provincia o comunidad y un año o rango.');
        return;
    }

    // Prepara datos para enviar
    const formData = new FormData();
    provincias.forEach(p => formData.append('provincias[]', p));
    comunidades.forEach(c => formData.append('comunidades[]', c));
    formData.append('anio', anio);
    formData.append('rango_check', rangoCheck);
    formData.append('rango_anios', rangoAnios);
    formData.append('mostrar_genero', mostrarGenero);
    formData.append('mostrar_mortalidad', mostrarMortalidad);

    // CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // CORRIGE la URL a la de tu vista Django
    fetch('/generar_grafica/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
      if (data.grafica_base64) {
        document.getElementById('grafica').src = 'data:image/png;base64,' + data.grafica_base64;
      }
    });
});


  document.querySelector('.btn-limpiar').addEventListener('click', function() {
    // Lógica para limpiar todos los filtros
    provinciaCheckboxes.forEach(checkbox => checkbox.checked = false);
    document.getElementById('anio').value = '';
    rangoCheck.checked = false;
    rangoInput.value = '';
    document.getElementById('filtro-genero').checked = false;
    document.getElementById('filtro-mortandad').checked = false;
  });
  
  const genero = document.getElementById('filtro-genero');
  const mortalidad = document.getElementById('filtro-mortalidad');

  if (genero && mortalidad) {
    genero.addEventListener('change', function() {
      if (this.checked) {
        mortalidad.checked = false;
      }
    });
    mortalidad.addEventListener('change', function() {
      if (this.checked) {
        genero.checked = false;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    const comHeader = document.getElementById('com-header');
    const comOptions = document.getElementById('com-options');

    // Alternar visibilidad al hacer clic en el header
    comHeader.addEventListener('click', function() {
        comOptions.classList.toggle('open');
    });

    // Cerrar el menú si se hace clic fuera
    document.addEventListener('click', function(e) {
        if (!comHeader.contains(e.target) && !comOptions.contains(e.target)) {
            comOptions.classList.remove('open');
        }
    });
});


});
