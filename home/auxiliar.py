def generar_grafica(request):
    # Recoge los filtros del frontend
    provincias = request.POST.getlist('provincias[]')
    comunidades = request.POST.getlist('comunidades[]')
    anio = request.POST.get('anio')
    rango_check = request.POST.get('rango_check')
    rango_anios = request.POST.get('rango_anios')
    mostrar_genero = request.POST.get('mostrar_genero') == 'true'
    mostrar_mortalidad = request.POST.get('mostrar_mortalidad') == 'true'

    # Validación: al menos provincia o comunidad y año o rango
    if (not provincias and not comunidades) or (not anio and not rango_anios):
        return JsonResponse({'error': 'Debes seleccionar al menos una provincia o comunidad y un año o rango.'})

    # Filtra tu queryset según los filtros recibidos (ejemplo)
    qs = Victima.objects.all()
    if provincias:
        qs = qs.filter(incidente__localidad__provincia__nombreProvincia=provincias)
    if comunidades:
        qs = qs.filter(incidente__localidad__provincia__codccaa__nombreccaa=comunidades)
    if rango_check == True:
        start, end = map(int, rango_anios.split('-'))
        qs = qs.filter(incidente__fechar__year__gte=start, incidente__fechar__year__lte=end)
    if rango_check == False:
        qs = qs.filter(incidente__fechar__year=anio)

        
    if mostrar_genero:
        df = pd.DataFrame(list(qs.values('incidente__localidad__provincia', 'incidente__localidad__provincia__codccaa__nombreccaa',
                                          'incidente__fecha__year', 'sexo')))
        color = 'genero'
    elif mostrar_mortalidad:
        df = pd.DataFrame(list(qs.values('incidente__localidad__provincia', 'incidente__localidad__provincia__codccaa__nombreccaa',
                                          'incidente__fecha__year', 'pronostico')))
        color = 'mortalidad'
    else:
        df = pd.DataFrame(list(qs.values('incidente__localidad__provincia', 'incidente__localidad__provincia__codccaa__nombreccaa',
                                          'incidente__fecha__year')))
        color = None
    
    print(df.info())  # Muestra nombres de columnas y tipos de datos



    # Eje X: provincia o comunidad según filtro
    if provincias:
        y = df.groupby('provincia').size().reset_index(name='num_ahogamientos')
        x = provincias
    else:
        y = df.groupby('incidente__localidad__provincia', 'incidente__localidad__provincia__codccaa__nombreccaa').size().reset_index(name='num_ahogamientos')
        x = comunidades
    
    max_ahogamientos = y['num_ahogamientos'].max() if not y.empty else 0
    scale_max = (max_ahogamientos // 10 + 1) * 10 if max_ahogamientos > 0 else 10
    scale_values = list(range(0, scale_max + 1, 10))

    # Crea la gráfica de barras apilada
    fig = px.bar(
        df,
        x=x,
        y='num_ahogamientos',
        color=color,
        barmode='stack',  # Apilada
        title='Gráfica de barras apilada'
    )

    fig.update_layout(
    yaxis=dict(
        tickmode='array',
        tickvals=scale_values,
        ticktext=[str(v) for v in scale_values]
    )
)

    # Devuelve el HTML de la gráfica
    return JsonResponse({'grafica_html': fig.to_html(full_html=False)})