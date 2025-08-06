document.addEventListener('DOMContentLoaded', function() {

    // Botones del selector de gráficas
    const buttons = document.querySelectorAll('.selector-graficas button');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            buttons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // IDs de los botones
    const botones = [
        'btn-grafica-apilada',
        'btn-grafica-circular',
        'btn-grafica-lineas',
        'btn-diagrama-dispersion',
        'btn-mapa',
        'btn-histograma',
        'btn-radar',
        'btn-analisis-automático',
        'btn-hotspots',
    ];

    // IDs de los filtros asociados, en el mismo orden que los botones
    const filtros = [
        'filtros-apilada',
        'filtros-circular',
        'filtros-lineas',
        'filtros-dispersion',
        'filtros-mapa',
        'filtros-histograma',
        'filtros-radar',
        'filtros-analisis-auto',
        'filtros-hotspots',
    ];

    // Asocia cada botón a su filtro, alternando visibilidad y clases
    botones.forEach((btnId, idx) => {
        document.getElementById(btnId).addEventListener('click', function() {
            filtros.forEach((filtroId, i) => {
                document.getElementById(filtroId).style.display = (i === idx) ? 'block' : 'none';
            });
            botones.forEach((bId, j) => {
                document.getElementById(bId).classList.toggle('active', j === idx);
            });
        });
    });


    // Multi-select de Comunidades
    const comHeader = document.getElementById('com-header');
    const comOptions = document.getElementById('com-options');
    const comPills = document.getElementById('com-pills');
    const comCheckboxes = comOptions.querySelectorAll('input[type="checkbox"]');

    // Multi-select de Provincias
    const provHeader = document.getElementById('prov-header');
    const provOptions = document.getElementById('prov-options');
    const provPills = document.getElementById('prov-pills');
    const provCheckboxes = provOptions.querySelectorAll('input[type="checkbox"]');

    // Control de bloqueo/desbloqueo
    function setProvinciasBloqueadas(bloquear) {
        provHeader.classList.toggle('disabled', bloquear);
        provHeader.setAttribute('tabindex', bloquear ? '-1' : '0');
        provCheckboxes.forEach(cb => cb.disabled = bloquear);
    }
    function setComunidadesBloqueadas(bloquear) {
        comHeader.classList.toggle('disabled', bloquear);
        comHeader.setAttribute('tabindex', bloquear ? '-1' : '0');
        comCheckboxes.forEach(cb => cb.disabled = bloquear);
    }

    // Abrir/cerrar menú comunidades
    comHeader.addEventListener('click', function(e) {
        if (comHeader.classList.contains('disabled')) return;
        comOptions.classList.toggle('open');
    });

    // Cerrado al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!comHeader.contains(e.target) && !comOptions.contains(e.target)) {
        comOptions.classList.remove('open');
        }
        if (!provHeader.contains(e.target) && !provOptions.contains(e.target)) {
        provOptions.classList.remove('open');
        }
    });

    // Abrir/cerrar menú provincias
    provHeader.addEventListener('click', function(e) {
        if (provHeader.classList.contains('disabled')) return;
        provOptions.classList.toggle('open');
    });

    // Actualizar pills de comunidades
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
            if (!document.querySelector('#com-options input[type="checkbox"]:checked')) {
                setProvinciasBloqueadas(false);
            }
            };
            pill.appendChild(remove);
            comPills.appendChild(pill);
        }
        });
        comHeader.textContent = selected.length > 0 ? `${selected.length} seleccionadas` : 'Selecciona comunidades';

        if (selected.length > 0) {
        setProvinciasBloqueadas(true);
        } else {
        setProvinciasBloqueadas(false);
        }
    }
    // Actualizar pills de provincias
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
            if (!document.querySelector('#prov-options input[type="checkbox"]:checked')) {
                setComunidadesBloqueadas(false);
            }
            };
            pill.appendChild(remove);
            provPills.appendChild(pill);
        }
        });
        provHeader.textContent = selected.length > 0 ? `${selected.length} seleccionadas` : 'Selecciona provincias';

        if (selected.length > 0) {
        setComunidadesBloqueadas(true);
        } else {
        setComunidadesBloqueadas(false);
        }
    }

    // Actualizar pills al cambiar cualquier checkbox
    comCheckboxes.forEach(cb => cb.addEventListener('change', updateComPills));
    provCheckboxes.forEach(cb => cb.addEventListener('change', updateProvPills));

    // Inicializar pills al cargar
    updateComPills();
    updateProvPills();

    // Diferenciar por sexo
    const colorSexoSwitch = document.getElementById('color-sexo-switch');

    // Filtrar por mortalidad
    const mortalSwitch = document.getElementById('mortal-switch');

    // Botón para limpiar filtros
    const clearGraficaApilada = document.getElementById('btn-limpiar-grafica-apilada');
    clearGraficaApilada.addEventListener('click', function() {
        document.querySelectorAll('#com-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.querySelectorAll('#prov-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.getElementById('anio').value = '';
        colorSexoSwitch.checked = false;
        mortalSwitch.checked = false;
        updateComPills();
        updateProvPills();
    });

    // Botón para generar la gráfica apilada
    const generateGraficaApilada = document.getElementById('btn-generar-grafica-apilada');
    generateGraficaApilada.addEventListener('click', function() {
        const comunidades = Array.from(document.querySelectorAll('#com-options input[type="checkbox"]:checked')).map(cb => cb.value);
        const provincias = Array.from(document.querySelectorAll('#prov-options input[type="checkbox"]:checked')).map(cb => cb.value);
        const anio = document.getElementById('anio').value;

        const formData = new FormData();
        if (comunidades.length > 0) {
        comunidades.forEach(c => formData.append('comunidades[]', c));
        } else {
        provincias.forEach(p => formData.append('provincias[]', p));
        }
        formData.append('anio', anio);
        formData.append('color_sexo', colorSexoSwitch.checked ? 'true' : 'false');
        formData.append('solo_mortales', mortalSwitch.checked ? 'true' : 'false');

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/generar_grafica_apilada/', {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
        const container = document.getElementById('grafica-container');
        container.innerHTML = '';
        if (data.grafica_html) {
            container.innerHTML = data.grafica_html;
            container.querySelectorAll('script').forEach(script => {
            const newScript = document.createElement('script');
            if (script.src) {
                newScript.src = script.src;
            } else {
                newScript.text = script.textContent;
            }
            document.body.appendChild(newScript);
            script.parentNode.removeChild(script);
            });
        } else if (data.error) {
            container.innerHTML = `<div class="error">${data.error}</div>`;
        }
        });
    });

    // Multi-select de Nacionalidades
    const nacHeader = document.getElementById('nacionalidad-header');
    const nacOptions = document.getElementById('nacionalidad-options');
    const nacPills = document.getElementById('nacionalidad-pills');
    const nacCheckboxes = nacOptions.querySelectorAll('input[type="checkbox"]');

    // Abrir/cerrar menú nacionalidades
    nacHeader.addEventListener('click', function(e) {
        if (nacHeader.classList.contains('disabled')) return;
        nacOptions.classList.toggle('open');
    });
    
    // Cerrado al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!nacHeader.contains(e.target) && !nacOptions.contains(e.target)) {
        nacOptions.classList.remove('open');
        }
    });

    // Función para actualizar las pills y el bloqueo
    function updateNacPills() {
        nacPills.innerHTML = '';
        let todas = nacOptions.querySelector('input[value="Todas"]');
        let selected = [];

        if (todas.checked) {
            nacCheckboxes.forEach(cb => {
            if (cb !== todas) {
                cb.checked = false;
                cb.disabled = true;
            }
            });
            const pill = document.createElement('span');
            pill.className = 'pill';
            pill.textContent = 'Todas';
            const remove = document.createElement('span');
            remove.className = 'pill-remove';
            remove.textContent = '×';
            remove.onclick = () => {
            todas.checked = false;
            nacCheckboxes.forEach(cb => cb.disabled = false);
            updateNacPills();
            };
            pill.appendChild(remove);
            nacPills.appendChild(pill);
            nacHeader.textContent = 'Todas seleccionadas';
            return;
        } else {
            nacCheckboxes.forEach(cb => cb.disabled = false);
        }
        nacCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
            selected.push(cb.parentElement.textContent.trim());
            const pill = document.createElement('span');
            pill.className = 'pill';
            pill.textContent = cb.parentElement.textContent.trim();
            const remove = document.createElement('span');
            remove.className = 'pill-remove';
            remove.textContent = '×';
            remove.onclick = () => {
                cb.checked = false;
                updateNacPills();
            };
            pill.appendChild(remove);
            nacPills.appendChild(pill);
            }
        });

        nacHeader.textContent = selected.length > 0
            ? `${selected.length} seleccionadas`
            : 'Selecciona nacionalidades';
    }

    // Actualiza las pills cuando se cambia cualquier checkbox de nacionalidad
    nacCheckboxes.forEach(cb => cb.addEventListener('change', updateNacPills));

    // Inicializa las pills al cargar por primera vez
    updateNacPills();

    // Botón para generar la gráfica circular
    const btnCircular = document.getElementById('btn-generar-grafica-circular');
    btnCircular.addEventListener('click', function() {
        const nacionalidadChecks = document.querySelectorAll('#nacionalidad-options input[type="checkbox"]:checked');
        const nacionalidades = Array.from(nacionalidadChecks).map(cb => cb.value).filter(v => v !== "");

        const anioInicio = document.getElementById('anio-inicio').value;
        const anioFin = document.getElementById('anio-fin').value;

        const formData = new FormData();
        nacionalidades.forEach(nac => formData.append('nacionalidades[]', nac)); 
        formData.append('anio_inicio', anioInicio);
        formData.append('anio_fin', anioFin);

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/generar_grafica_circular/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('grafica-container');
            container.innerHTML = '';
            if (data.grafica_html) {
            container.innerHTML = data.grafica_html;
            container.querySelectorAll('script').forEach(script => {
                const newScript = document.createElement('script');
                if (script.src) { newScript.src = script.src; }
                else { newScript.text = script.textContent; }
                document.body.appendChild(newScript);
                script.parentNode.removeChild(script);
            });
            } else if (data.error) {
            container.innerHTML = `<p class="error">${data.error}</p>`;
            }
        });
    });

    // Botón para limpiar filtros
    const clearGraficaCircular = document.getElementById('btn-limpiar-grafica-circular');
    clearGraficaCircular.addEventListener('click', function() {
        document.querySelectorAll('#nacionalidad-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.getElementById('anio-inicio').value = '';
        document.getElementById('anio-fin').value = '';
        updateNacPills();
    });

    // Botón para generar la gráfica de líneas
    const generateGraficaLineas = document.getElementById('btn-generar-grafica-lineas');
    generateGraficaLineas.addEventListener('click', function() {
        const anio = document.getElementById('anio-lineas').value;
        const soloMortales = document.getElementById('mortal-switch-lineas').checked;

        const formData = new FormData();
        formData.append('anio', anio);
        formData.append('solo_mortales', soloMortales ? 'true' : 'false');

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/generar_grafica_lineas/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('grafica-container');
            container.innerHTML = '';
            if (data.grafica_html) {
                container.innerHTML = data.grafica_html;
                container.querySelectorAll('script').forEach(script => {
                    const newScript = document.createElement('script');
                    if (script.src) {
                        newScript.src = script.src;
                    } else {
                        newScript.text = script.textContent;
                    }
                    document.body.appendChild(newScript);
                    script.parentNode.removeChild(script);
                });
            } else if (data.error) {
                container.innerHTML = `<div class="error">${data.error}</div>`;
            }
        });
    });

    // Botón para limpiar filtros
    const clearGraficaLineas = document.getElementById('btn-limpiar-grafica-lineas');
    clearGraficaLineas.addEventListener('click', function() {
        document.getElementById('anio-lineas').value = '';
        document.getElementById('mortal-switch-lineas').checked = false;
    });

    // Botón para limpiar filtros
    const clearDiagramaDispersion = document.getElementById('btn-limpiar-diagrama-dispersion');
    clearDiagramaDispersion.addEventListener('click', function() {
        document.getElementById('color-sexo-switch-dispersion').checked = false;
        document.getElementById('mortal-switch-dispersion').checked = false;
        document.getElementById('linea-dispersion').checked = false;
    });

    // Botón para generar el diagrama de dispersión
    const generateDiagramaDispersion = document.getElementById('btn-generar-diagrama-dispersion');
    generateDiagramaDispersion.addEventListener('click', function() {
        const soloMortales = document.getElementById('mortal-switch-dispersion').checked;
        const filtraSexo = document.getElementById('color-sexo-switch-dispersion').checked;
        const linea = document.getElementById('linea-dispersion').checked;

        const formData = new FormData();
        formData.append('solo_mortales', soloMortales ? 'true' : 'false');
        formData.append('color_sexo', filtraSexo ? 'true' : 'false');
        formData.append('mostrar_linea', linea ? 'true' : 'false');

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/generar_diagrama_dispersion/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('grafica-container');
            container.innerHTML = '';
            if (data.grafica_html) {
                container.innerHTML = data.grafica_html;
                container.querySelectorAll('script').forEach(script => {
                    const newScript = document.createElement('script');
                    if (script.src) {
                        newScript.src = script.src;
                    } else {
                        newScript.text = script.textContent;
                    }
                    document.body.appendChild(newScript);
                    script.parentNode.removeChild(script);
                });
            } else if (data.error) {
                container.innerHTML = `<div class="error">${data.error}</div>`;
            }
        });
    });

    // Multi-select de lugares
    const lugHeader = document.getElementById('lugar-header');
    const lugOptions = document.getElementById('lugar-options');
    const lugPills = document.getElementById('lugar-pills');
    const lugCheckboxes = lugOptions.querySelectorAll('input[type="checkbox"]');

    // Abrir/cerrar menú lugares
    lugHeader.addEventListener('click', function(e) {
        if (lugHeader.classList.contains('disabled')) return;
        lugOptions.classList.toggle('open');
    });

    // Cerrado al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!lugHeader.contains(e.target) && !lugOptions.contains(e.target)) {
        lugOptions.classList.remove('open');
        }
    });

    // Función para actualizar las pills y el bloqueo para lugares
    function updateLugPills() {
        lugPills.innerHTML = '';
        let todas = lugOptions.querySelector('input[value="Todos"]');
        let selected = [];

        if (todas.checked) {
            lugCheckboxes.forEach(cb => {
                if (cb !== todas) {
                    cb.checked = false;
                    cb.disabled = true;
                }
            });
            const pill = document.createElement('span');
            pill.className = 'pill';
            pill.textContent = 'Todos';
            const remove = document.createElement('span');
            remove.className = 'pill-remove';
            remove.textContent = '×';
            remove.onclick = () => {
                todas.checked = false;
                lugCheckboxes.forEach(cb => cb.disabled = false);
                updateLugPills();
            };
            pill.appendChild(remove);
            lugPills.appendChild(pill);
            lugHeader.textContent = 'Todos seleccionados';
            return;
        } else {
            lugCheckboxes.forEach(cb => cb.disabled = false);
        }

        lugCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                selected.push(cb.parentElement.textContent.trim());
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = cb.parentElement.textContent.trim();
                const remove = document.createElement('span');
                remove.className = 'pill-remove';
                remove.textContent = '×';
                remove.onclick = () => {
                    cb.checked = false;
                    updateLugPills();
                };
                pill.appendChild(remove);
                lugPills.appendChild(pill);
            }
        });

        lugHeader.textContent = selected.length > 0
            ? `${selected.length} seleccionados`
            : 'Selecciona lugares';
    }

    // Actualiza las pills cuando se cambia cualquier checkbox de lugar
    lugCheckboxes.forEach(cb => cb.addEventListener('change', updateLugPills));

    // Inicializa las pills al cargar por primera vez
    updateLugPills();

    // Limpiar los filtros
    const clearMapa = document.getElementById('btn-limpiar-mapa');
    clearMapa.addEventListener('click', function() {
        document.querySelectorAll('#lugar-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.getElementById('mortal-switch-mapa').checked = false;
        updateLugPills();
    });
    
    // Botón para generar el mapa
    const generateMapa = document.getElementById('btn-generar-mapa');
    generateMapa.addEventListener('click', function() {
        const soloMortales = document.getElementById('mortal-switch-mapa').checked;

        const lugarCheckboxes = document.querySelectorAll('#lugar-options input[type=checkbox]');
        let lugaresSeleccionados = [];
        lugarCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                lugaresSeleccionados.push(cb.value);
            }
        });

        const formData = new FormData();
        formData.append('solo_mortales', soloMortales ? 'true' : 'false');
        lugaresSeleccionados.forEach(lugar => formData.append('lugares[]', lugar));

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/generar_mapa/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('grafica-container');
            container.innerHTML = '';
            if (data.grafica_html) {
                container.innerHTML = data.grafica_html;
                container.querySelectorAll('script').forEach(script => {
                    const newScript = document.createElement('script');
                    if (script.src) {
                        newScript.src = script.src;
                    } else {
                        newScript.text = script.textContent;
                    }
                    document.body.appendChild(newScript);
                    script.parentNode.removeChild(script);
                });
            } else if (data.error) {
                container.innerHTML = `<div class="error">${data.error}</div>`;
            }
        });
    });

    // Multi-select de días de la semana para el histograma
    const diaHeader = document.getElementById('dia-header');
    const diaOptions = document.getElementById('dia-options');
    const diaPills = document.getElementById('dia-pills');
    const diaCheckboxes = diaOptions.querySelectorAll('input[type="checkbox"]');

    // Abrir/cerrar menú días
    diaHeader.addEventListener('click', function(e) {
        if (diaHeader.classList.contains('disabled')) return;
        diaOptions.classList.toggle('open');
    });

    // Cerrado al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!diaHeader.contains(e.target) && !diaOptions.contains(e.target)) {
            diaOptions.classList.remove('open');
        }
    });

    // Función para actualizar las pills y el bloqueo para días
    function updateDiaPills() {
        diaPills.innerHTML = '';
        let todos = diaOptions.querySelector('input[value="Todos"]');
        let selected = [];

        if (todos.checked) {
            diaCheckboxes.forEach(cb => {
                if (cb !== todos) {
                    cb.checked = false;
                    cb.disabled = true;
                }
            });
            const pill = document.createElement('span');
            pill.className = 'pill';
            pill.textContent = 'Todos';
            const remove = document.createElement('span');
            remove.className = 'pill-remove';
            remove.textContent = '×';
            remove.onclick = () => {
                todos.checked = false;
                diaCheckboxes.forEach(cb => cb.disabled = false);
                updateDiaPills();
            };
            pill.appendChild(remove);
            diaPills.appendChild(pill);
            diaHeader.textContent = 'Todos seleccionados';
            return;
        } else {
            diaCheckboxes.forEach(cb => cb.disabled = false);
        }

        diaCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                selected.push(cb.parentElement.textContent.trim());
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = cb.parentElement.textContent.trim();
                const remove = document.createElement('span');
                remove.className = 'pill-remove';
                remove.textContent = '×';
                remove.onclick = () => {
                    cb.checked = false;
                    updateDiaPills();
                };
                pill.appendChild(remove);
                diaPills.appendChild(pill);
            }
        });

        diaHeader.textContent = selected.length > 0
            ? `${selected.length} seleccionados`
            : 'Selecciona días';
    }

    // Actualiza las pills cuando se cambia cualquier checkbox de día
    diaCheckboxes.forEach(cb => cb.addEventListener('change', updateDiaPills));

    // Inicializa las pills al cargar
    updateDiaPills();

    // Limpiar los filtros
    const clearHistograma = document.getElementById('btn-limpiar-histograma');
    clearHistograma.addEventListener('click', function() {
        document.querySelectorAll('#dia-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.getElementById('mortal-switch-histograma').checked = false;
        updateDiaPills();
    });

    // Botón para generar el histograma
    const generateHistograma = document.getElementById('btn-generar-histograma');
    generateHistograma.addEventListener('click', function() {
        const soloMortales = document.getElementById('mortal-switch-histograma').checked;

        const diaCheckboxes = document.querySelectorAll('#dia-options input[type=checkbox]');
        let diasSeleccionados = [];
        diaCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                diasSeleccionados.push(cb.value);
            }
        });

        const formData = new FormData();
        formData.append('solo_mortales', soloMortales ? 'true' : 'false');
        diasSeleccionados.forEach(dia => formData.append('dias[]', dia));

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/generar_histograma/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('grafica-container');
            container.innerHTML = '';
            if (data.grafica_html) {
                container.innerHTML = data.grafica_html;
                container.querySelectorAll('script').forEach(script => {
                    const newScript = document.createElement('script');
                    if (script.src) {
                        newScript.src = script.src;
                    } else {
                        newScript.text = script.textContent;
                    }
                    document.body.appendChild(newScript);
                    script.parentNode.removeChild(script);
                });
            } else if (data.error) {
                container.innerHTML = `<div class="error">${data.error}</div>`;
            }
        });
    });

    // Multi-select de filtro único para el radar
    const filtroHeader = document.getElementById('filtro-header');
    const filtroOptions = document.getElementById('filtro-options');
    const filtroPills = document.getElementById('filtro-pills');
    const filtroCheckboxes = filtroOptions.querySelectorAll('input[type="checkbox"]');

    // Abrir/cerrar menú de filtros
    filtroHeader.addEventListener('click', function(e) {
        if (filtroHeader.classList.contains('disabled')) return;
        filtroOptions.classList.toggle('open');
    });

    // Cerrado al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!filtroHeader.contains(e.target) && !filtroOptions.contains(e.target)) {
            filtroOptions.classList.remove('open');
        }
    });

    // Función para actualizar la pill y bloquear para filtro único
    function updateFiltroPills() {
        filtroPills.innerHTML = '';
        let selected = [];

        let checked = Array.from(filtroCheckboxes).find(cb => cb.checked);
        filtroCheckboxes.forEach(cb => {
            if (checked && cb !== checked) {
                cb.disabled = true;
            } else {
                cb.disabled = false;
            }
        });

        if (checked) {
            selected.push(checked.parentElement.textContent.trim());
            const pill = document.createElement('span');
            pill.className = 'pill';
            pill.textContent = checked.parentElement.textContent.trim();
            const remove = document.createElement('span');
            remove.className = 'pill-remove';
            remove.textContent = '×';
            remove.onclick = function(e) {
                e.stopPropagation();
                checked.checked = false;
                updateFiltroPills();
            };
            pill.appendChild(remove);
            filtroPills.appendChild(pill);
            filtroHeader.textContent = selected[0];
        } else {
            filtroHeader.textContent = 'Selecciona filtro';
        }
    }

    // Al cambiar cualquier filtro, actualizar pill única
    filtroCheckboxes.forEach(cb => cb.addEventListener('change', function() {
        if (this.checked) {
            filtroCheckboxes.forEach(cb2 => {
                if (cb2 !== this) cb2.checked = false;
            });
        }
        updateFiltroPills();
    }));

    // Inicializa la pill/filtro al cargar
    updateFiltroPills();

    // Limpiar filtro radar
    const clearRadar = document.getElementById('btn-limpiar-radar');
    clearRadar.addEventListener('click', function() {
        filtroCheckboxes.forEach(cb => cb.checked = false);
        updateFiltroPills();
    });

    // Generar radar
    const generateRadar = document.getElementById('btn-generar-radar');
    generateRadar.addEventListener('click', function() {
        let filtroSeleccionado = Array.from(filtroCheckboxes).find(cb => cb.checked);
        if (!filtroSeleccionado) {
            return;
        }

        const formData = new FormData();
        formData.append('filtro', filtroSeleccionado.value);

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/generar_radar/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('grafica-container');
            container.innerHTML = '';
            if (data.grafica_html) {
                container.innerHTML = data.grafica_html;
                container.querySelectorAll('script').forEach(script => {
                    const newScript = document.createElement('script');
                    if (script.src) {
                        newScript.src = script.src;
                    } else {
                        newScript.text = script.textContent;
                    }
                    document.body.appendChild(newScript);
                    script.parentNode.removeChild(script);
                });
            } else if (data.error) {
                container.innerHTML = `<div class="error">${data.error}</div>`;
            }
        });
    });

    // Función para hacer multi-select single-choice
    function setSingleChoiceMultiSelect(groupId, updatePillsFunction) {
        const options = document.querySelectorAll(`#${groupId}-options input[type="checkbox"]`);
        options.forEach(cb => {
            cb.addEventListener('change', () => {
                if (cb.checked) {
                    options.forEach(otherCb => {
                        if (otherCb !== cb) otherCb.checked = false;
                    });
                }
                if (typeof updatePillsFunction === 'function') updatePillsFunction();
            });
        });
    }

    // Multi-select de Actividad
    const actividadHeader = document.getElementById('actividad-header');
    const actividadOptions = document.getElementById('actividad-options');
    const actividadPills = document.getElementById('actividad-pills');
    const actividadCheckboxes = actividadOptions.querySelectorAll('input[type="checkbox"]');

    // Abrir/cerrar menú de filtros
    actividadHeader.addEventListener('click', function(e) {
        if (actividadHeader.classList.contains('disabled')) return;
        actividadOptions.classList.toggle('open');
    });

    // Cerrado al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!actividadHeader.contains(e.target) && !actividadOptions.contains(e.target)) {
            actividadOptions.classList.remove('open');
        }
    });

    // Función para actualizar la pill y bloquear para filtro único
    function updateActividadPills() {
        actividadPills.innerHTML = '';
        const selected = [];
        actividadCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                selected.push(cb.parentElement.textContent.trim());
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = cb.parentElement.textContent.trim();
                const remove = document.createElement('span');
                remove.className = 'pill-remove';
                remove.textContent = '×';
                remove.onclick = () => {
                    cb.checked = false;
                    updateActividadPills();
                };
                pill.appendChild(remove);
                actividadPills.appendChild(pill);
            }
        });
        actividadHeader.textContent = selected.length > 0 ? `${selected.length} seleccionada` : 'Selecciona actividad';
    }

    // Al cambiar cualquier filtro, actualizar pill única
    actividadCheckboxes.forEach(cb => cb.addEventListener('change', updateActividadPills));

    // Inicializa la pill/filtro al cargar
    updateActividadPills();

    // Inicializa un selector de elección simple con multiselección para el campo 'actividad'
    setSingleChoiceMultiSelect('actividad', updateActividadPills);


    // Multi-select de Localización
    const localizacionHeader = document.getElementById('localizacion-header');
    const localizacionOptions = document.getElementById('localizacion-options');
    const localizacionPills = document.getElementById('localizacion-pills');
    const localizacionCheckboxes = localizacionOptions.querySelectorAll('input[type="checkbox"]');

    localizacionHeader.addEventListener('click', function(e) {
        if (localizacionHeader.classList.contains('disabled')) return;
        localizacionOptions.classList.toggle('open');
    });


    document.addEventListener('click', function(e) {
        if (!localizacionHeader.contains(e.target) && !localizacionOptions.contains(e.target)) {
            localizacionOptions.classList.remove('open');
        }
    });


    function updateLocalizacionPills() {
        localizacionPills.innerHTML = '';
        const selected = [];
        localizacionCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                selected.push(cb.parentElement.textContent.trim());
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = cb.parentElement.textContent.trim();
                const remove = document.createElement('span');
                remove.className = 'pill-remove';
                remove.textContent = '×';
                remove.onclick = () => {
                    cb.checked = false;
                    updateLocalizacionPills();
                };
                pill.appendChild(remove);
                localizacionPills.appendChild(pill);
            }
        });
        localizacionHeader.textContent = selected.length > 0 ? `${selected.length} seleccionada` : 'Selecciona localización';
    }


    localizacionCheckboxes.forEach(cb => cb.addEventListener('change', updateLocalizacionPills));


    updateLocalizacionPills();
    
    setSingleChoiceMultiSelect('localizacion', updateLocalizacionPills);


    // ==== Multi-select de Zona Vigilada ====
    const zonaHeader = document.getElementById('zonavigilada-header');
    const zonaOptions = document.getElementById('zonavigilada-options');
    const zonaPills = document.getElementById('zonavigilada-pills');
    const zonaCheckboxes = zonaOptions.querySelectorAll('input[type="checkbox"]');

    zonaHeader.addEventListener('click', function(e) {
        if (zonaHeader.classList.contains('disabled')) return;
        zonaOptions.classList.toggle('open');
    });
    document.addEventListener('click', function(e) {
        if (!zonaHeader.contains(e.target) && !zonaOptions.contains(e.target)) {
            zonaOptions.classList.remove('open');
        }
    });
    function updateZonaPills() {
        zonaPills.innerHTML = '';
        const selected = [];
        zonaCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                selected.push(cb.parentElement.textContent.trim());
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = cb.parentElement.textContent.trim();
                const remove = document.createElement('span');
                remove.className = 'pill-remove';
                remove.textContent = '×';
                remove.onclick = () => {
                    cb.checked = false;
                    updateZonaPills();
                };
                pill.appendChild(remove);
                zonaPills.appendChild(pill);
            }
        });
        zonaHeader.textContent = selected.length > 0 ? `${selected.length} seleccionada` : 'Selecciona opción';
    }
    zonaCheckboxes.forEach(cb => cb.addEventListener('change', updateZonaPills));
    updateZonaPills();
    setSingleChoiceMultiSelect('zonavigilada', updateZonaPills);


    // ==== Multi-select de Riesgo ====
    const riesgoHeader = document.getElementById('riesgo-header');
    const riesgoOptions = document.getElementById('riesgo-options');
    const riesgoPills = document.getElementById('riesgo-pills');
    const riesgoCheckboxes = riesgoOptions.querySelectorAll('input[type="checkbox"]');

    riesgoHeader.addEventListener('click', function(e) {
        if (riesgoHeader.classList.contains('disabled')) return;
        riesgoOptions.classList.toggle('open');
    });
    document.addEventListener('click', function(e) {
        if (!riesgoHeader.contains(e.target) && !riesgoOptions.contains(e.target)) {
            riesgoOptions.classList.remove('open');
        }
    });
    function updateRiesgoPills() {
        riesgoPills.innerHTML = '';
        const selected = [];
        riesgoCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                selected.push(cb.parentElement.textContent.trim());
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = cb.parentElement.textContent.trim();
                const remove = document.createElement('span');
                remove.className = 'pill-remove';
                remove.textContent = '×';
                remove.onclick = () => {
                    cb.checked = false;
                    updateRiesgoPills();
                };
                pill.appendChild(remove);
                riesgoPills.appendChild(pill);
            }
        });
        riesgoHeader.textContent = selected.length > 0 ? `${selected.length} seleccionada` : 'Selecciona riesgo';
    }
    riesgoCheckboxes.forEach(cb => cb.addEventListener('change', updateRiesgoPills));
    updateRiesgoPills();
    setSingleChoiceMultiSelect('riesgo', updateRiesgoPills);


    // ==== Multi-select de Intervención ====
    const intervencionHeader = document.getElementById('intervencion-header');
    const intervencionOptions = document.getElementById('intervencion-options');
    const intervencionPills = document.getElementById('intervencion-pills');
    const intervencionCheckboxes = intervencionOptions.querySelectorAll('input[type="checkbox"]');

    intervencionHeader.addEventListener('click', function(e) {
        if (intervencionHeader.classList.contains('disabled')) return;
        intervencionOptions.classList.toggle('open');
    });
    document.addEventListener('click', function(e) {
        if (!intervencionHeader.contains(e.target) && !intervencionOptions.contains(e.target)) {
            intervencionOptions.classList.remove('open');
        }
    });
    function updateIntervencionPills() {
        intervencionPills.innerHTML = '';
        const selected = [];
        intervencionCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== '') {
                selected.push(cb.parentElement.textContent.trim());
                const pill = document.createElement('span');
                pill.className = 'pill';
                pill.textContent = cb.parentElement.textContent.trim();
                const remove = document.createElement('span');
                remove.className = 'pill-remove';
                remove.textContent = '×';
                remove.onclick = () => {
                    cb.checked = false;
                    updateIntervencionPills();
                };
                pill.appendChild(remove);
                intervencionPills.appendChild(pill);
            }
        });
        intervencionHeader.textContent = selected.length > 0 ? `${selected.length} seleccionada` : 'Selecciona intervención';
    }
    intervencionCheckboxes.forEach(cb => cb.addEventListener('change', updateIntervencionPills));
    updateIntervencionPills();
    setSingleChoiceMultiSelect('intervencion', updateIntervencionPills);


    // ==== Botón limpiar filtros sklearn ====
    const clearSklearn = document.getElementById('btn-limpiar-sklearn');
    clearSklearn.addEventListener('click', function() {
        document.querySelectorAll('#actividad-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.querySelectorAll('#localizacion-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.querySelectorAll('#zonavigilada-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.querySelectorAll('#riesgo-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.querySelectorAll('#intervencion-options input[type="checkbox"]').forEach(cb => cb.checked = false);
        document.getElementById('edad-caso').value = '';
        updateActividadPills();
        updateLocalizacionPills();
        updateZonaPills();
        updateRiesgoPills();
        updateIntervencionPills();
    });

     // ==== Botón para comparar caso (enviar al backend sklearn y mostrar gráfica comparativa) ====
    const btnGenerarSklearn = document.getElementById('btn-generar-sklearn');
    btnGenerarSklearn.addEventListener('click', function() {
        const actividadChecked = document.querySelector('#actividad-options input[type="checkbox"]:checked');
        const localizacionChecked = document.querySelector('#localizacion-options input[type="checkbox"]:checked');
        const zonavigiladaChecked = document.querySelector('#zonavigilada-options input[type="checkbox"]:checked');
        const riesgoChecked = document.querySelector('#riesgo-options input[type="checkbox"]:checked');
        const intervencionChecked = document.querySelector('#intervencion-options input[type="checkbox"]:checked');
        const edad = document.getElementById('edad-caso').value.trim();


        const formData = new FormData();
        if (actividadChecked)    formData.append('actividad', actividadChecked.value);
        if (localizacionChecked) formData.append('localizacion', localizacionChecked.value);
        if (zonavigiladaChecked) formData.append('zonavigilada', zonavigiladaChecked.value);
        if (riesgoChecked)       formData.append('factorriesgo', riesgoChecked.value);
        if (intervencionChecked) formData.append('intervencion', intervencionChecked.value);
        if (edad)                formData.append('edad', edad);


        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/comparativa_sklearn/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('grafica-container');
            container.innerHTML = '';
            if (data.grafica_html) {
                container.innerHTML = data.grafica_html;
                container.querySelectorAll('script').forEach(script => {
                    const newScript = document.createElement('script');
                    if (script.src) { newScript.src = script.src; }
                    else { newScript.text = script.textContent; }
                    document.body.appendChild(newScript);
                    script.parentNode.removeChild(script);
                });
            } else if (data.error) {
                container.innerHTML = `<p class="error">${data.error}</p>`;
            }
        });
    });

    // Botón para limpiar filtros
    const clearMapaHotspots = document.getElementById('btn-limpiar-hotspots');
    clearMapaHotspots.addEventListener('click', function() {
        document.getElementById('anio-inicio-hotspots').value = '';
        document.getElementById('anio-fin-hotspots').value = '';
    });

    function pintarMapaHotspots(clusters) {
        if (!window.L) { console.error('Leaflet no está cargado'); return; }
        var mapDiv = document.getElementById('mapa-hotspots');
        if (!mapDiv) { console.error('El div mapa-hotspots NO existe'); return; }

        var mapDiv = document.getElementById('mapa-hotspots');
        mapDiv.innerHTML = ""; // Limpia si hace falta

        var map = L.map('mapa-hotspots').setView([43.46, -3.81], 9);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 17,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        clusters.forEach(c => {
            if (c.center_lat && c.center_lon) {
            L.circleMarker([c.center_lat, c.center_lon], {
                radius: 18,
                fillColor: "#ff8c00",
                color: "#222",
                fillOpacity: 0.7,
                weight: 2
            }).addTo(map)
            .bindPopup(`
                <b>Hotspot</b><br>
                Localidad: ${c.main_place}<br>
                Incidentes: ${c.total_incidents}<br>
                Mes más común: ${c.most_common_month}<br>
                Mortalidad: ${c.mortality_rate}%
            `);
            }
        });
    }


    const btnMapaHotspots = document.getElementById('btn-generar-hotspots');
    btnMapaHotspots.addEventListener('click', function() {
        const anioInicio = document.getElementById('anio-inicio-hotspots').value;
        const anioFin = document.getElementById('anio-fin-hotspots').value;

        const formData = new FormData();
        formData.append('anio-inicio-hotspots', anioInicio);
        formData.append('anio-fin-hotspots', anioFin);

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch('/generar_mapa_hotspots/', {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': csrftoken }
        })
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('grafica-container');
            container.innerHTML = '';
            if (data.html) {  // asegúrate que la clave aquí es 'html', no 'grafica_html'
                container.innerHTML = data.html;
                // Cuando el DOM ya tiene el div del mapa:
                if (data.clusters && data.clusters.length > 0) {
                    pintarMapaHotspots(data.clusters);
                } else {
                    // Opcional: muestra aviso si no hay clusters para pintar
                    console.log('No hay clusters para el mapa');
                }
            } else if (data.error) {
                container.innerHTML = `<p class="error">${data.error}</p>`;
            }
        });
    });
});