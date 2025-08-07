from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from .models import Victima
from .utils import obtener_codigo
import plotly as plotly
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, Label, GeoJSONDataSource, ColorBar, BasicTicker, PrintfTickFormatter
from bokeh.palettes import Category20c
from bokeh.transform import cumsum, factor_cmap, linear_cmap
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.transform import dodge
import numpy as np
from scipy.interpolate import make_interp_spline
import geopandas as gpd
from bokeh.palettes import Reds256
from django.db.models.functions import ExtractWeekDay
from itertools import cycle
from django.views.decorators.csrf import csrf_exempt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA
from datetime import datetime
from sklearn.cluster import DBSCAN


def home(request):
    return render(request, 'home.html')

@csrf_exempt
def generar_grafica_apilada(request):
    comunidades = request.POST.getlist('comunidades[]')
    provincias = request.POST.getlist('provincias[]')
    anio = request.POST.get('anio')
    color_sexo = request.POST.get('color_sexo') == 'true'
    solo_mortales = request.POST.get('solo_mortales') == 'true'

    if (not comunidades and not provincias) or not anio:
        return JsonResponse({'error': 'Selecciona al menos una comunidad o provincia y un año.'})

    if comunidades:
        codigos = [obtener_codigo("CCAA", comunidad) for comunidad in comunidades]
        agrupacion = 'incidente__localidad__provincia__codccaa__nombreccaa'
        etiqueta_x = "Comunidad"
        filtro = {'incidente__localidad__provincia__codccaa__in': codigos}
    else:
        codigos = [obtener_codigo("PROVINCIA", provincia) for provincia in provincias]
        agrupacion = 'incidente__localidad__provincia__nombreprovincia'
        etiqueta_x = "Provincia"
        filtro = {'incidente__localidad__provincia__codprovincia__in': codigos}
    filtro['incidente__fecha__year'] = anio

    if solo_mortales:
        filtro['pronostico__nombrepronostico'] = "Ahogamiento mortal"

    if color_sexo:
        qs = (
            Victima.objects
            .filter(**filtro)
            .values(agrupacion, 'sexo')
            .annotate(Ahogamientos=Count('codvictima'))
        )

        df = pd.DataFrame(list(qs))
        if df.empty:
            return JsonResponse({'error': 'No hay datos para esos filtros.'})

        df = df.pivot_table(index=agrupacion, columns='sexo', values='Ahogamientos', fill_value=0).reset_index()

        nombres = list(df[agrupacion])
        source = ColumnDataSource(df)

        p = figure(
            x_range=nombres,
            title=f'Ahogamientos por {etiqueta_x} en {anio}',
            x_axis_label=etiqueta_x,
            y_axis_label='Número de ahogamientos',
            height=400,
            width=700,
            toolbar_location='right',
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        bar_width = 0.33

        p.vbar(
            x=dodge(agrupacion, -0.17, range=p.x_range),
            top='Hombre',
            width=bar_width,
            source=source,
            legend_label="Hombres",
            color="#1976d2"
        )
        p.vbar(
            x=dodge(agrupacion, 0.17, range=p.x_range),
            top='Mujer',
            width=bar_width,
            source=source,
            legend_label="Mujeres",
            color="#d32f2f"
        )
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"
        hover = HoverTool(tooltips=[
            (etiqueta_x, f'@{agrupacion}'),
            ("Hombres", "@Hombre"),
            ("Mujeres", "@Mujer")
        ])
        p.add_tools(hover)
        p.x_range.range_padding = 0.05

    else:
        qs = (
            Victima.objects
            .filter(**filtro)
            .values(agrupacion)
            .annotate(Ahogamientos=Count('codvictima'))
        )

        df = pd.DataFrame(list(qs))

        if df.empty:
            return JsonResponse({'error': 'No hay datos para esos filtros.'})

        nombres = list(df[agrupacion])
        source = ColumnDataSource(df)

        p = figure(
            x_range=nombres,
            title=f'Ahogamientos por {etiqueta_x} en {anio}',
            x_axis_label=etiqueta_x,
            y_axis_label='Número de ahogamientos',
            height=400,
            width=700,
            toolbar_location='right',
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        p.vbar(x=agrupacion, top='Ahogamientos', width=0.6, source=source, color="#718dbf")
        labels = LabelSet(
            x=agrupacion,
            y='Ahogamientos',
            text='Ahogamientos',
            level='glyph',
            x_offset=0,
            y_offset=-10,
            text_align='center',
            text_baseline='middle',
            text_color='white',
            source=source
        )
        p.add_layout(labels)
        hover = HoverTool(tooltips=[
            (etiqueta_x, f'@{agrupacion}'),
            ("Ahogamientos", "@Ahogamientos")
        ])
        p.add_tools(hover)

    script, div = components(p)
    resources = CDN.render()
    return JsonResponse({
        'grafica_html': f"{resources}\n{script}\n{div}"
    })

@csrf_exempt
def generar_grafica_circular(request):
    nacionalidades = request.POST.getlist('nacionalidades[]')
    anio_inicio = request.POST.get('anio_inicio')
    anio_fin = request.POST.get('anio_fin')

   
    if anio_fin < anio_inicio:
        return JsonResponse({'error': 'El año de fin no puede ser inferior al de inicio.'})
    
    if not nacionalidades or not anio_inicio or not anio_fin or isinstance(anio_inicio, int) or isinstance(anio_fin, int):
        return JsonResponse({'error': 'Debes seleccionar al menos una nacionalidad y un rango de años válido.'})

    filtro = {
        "incidente__fecha__year__gte": anio_inicio,
        "incidente__fecha__year__lte": anio_fin
    }

    if nacionalidades and nacionalidades != ["Todas"]:
        filtro['nacionalidad__nombrenacionalidad__in'] = nacionalidades
       
    qs = (
        Victima.objects.filter(**filtro)
        .values('nacionalidad__nombrenacionalidad')
        .annotate(Ahogamientos=Count('codvictima'))
        .order_by('-Ahogamientos')
    )
    df = pd.DataFrame(list(qs))
    if df.empty:
        return JsonResponse({'error': 'No hay datos para esos filtros.'})


    df['nacionalidad__nombrenacionalidad'] = df['nacionalidad__nombrenacionalidad'].replace('', 'Sin datos')
    df = df.rename(columns={
        'nacionalidad__nombrenacionalidad': 'Nacionalidad',
        'Ahogamientos': 'Número de ahogamientos'
    })


    total = df['Número de ahogamientos'].sum()
    df['Porcentaje'] = df['Número de ahogamientos'] / total * 100
    df_principales = df[df['Porcentaje'] >= 2].copy()
    df_otros = df[df['Porcentaje'] < 2]
    nacionalidades_otras = ''
    if not df_otros.empty:
        suma_otros = df_otros['Número de ahogamientos'].sum()
        top5_otros = (df_otros.sort_values('Número de ahogamientos', ascending=False).head(5)['Nacionalidad'].tolist())
        nacionalidades_otras = ", ".join(top5_otros)
        if len(df_otros) > 5:
            nacionalidades_otras += "…"
        df_principales = pd.concat([
            df_principales,
            pd.DataFrame({
                'Nacionalidad': ['Otras'],
                'Número de ahogamientos': [suma_otros],
                'Porcentaje': [suma_otros / total * 100]
            })
        ], ignore_index=True)


    n = len(df_principales)
    palette_raw = Category20c[max(3, min(n, 20))]
    df_principales['color'] = [c for _, c in zip(range(n), cycle(palette_raw))]
    df_principales['angle'] = df_principales['Número de ahogamientos'] / df_principales['Número de ahogamientos'].sum() * 2 * np.pi
    df_principales['customtext'] = [
        f"Nacionalidades recogidas en Otras: {nacionalidades_otras}" if n == 'Otras' and nacionalidades_otras else ''
        for n in df_principales['Nacionalidad']
    ]


    source = ColumnDataSource(df_principales)
    titulo = f"Distribución de ahogamientos por nacionalidad ({anio_inicio} - {anio_fin})"


    p = figure(
        height=450, 
        width=620, 
        title=titulo,
        x_range=(-0.45, 1.05),
        background_fill_color="#fafafa",
        toolbar_location='right',
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )
    p.title.align = "center"
    p.title.text_font_size = "18px"
    p.title.text_font_style = "bold"


    p.wedge(
        x=0, y=1, radius=0.42,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color="white", fill_color='color',
        legend_field='Nacionalidad', source=source
    )


    p.axis.visible = False
    p.grid.grid_line_color = None


    tooltips = "@Nacionalidad: @{Número de ahogamientos} ahogamientos<br>@Porcentaje{0.2f}%<br>@customtext"
    hover = HoverTool(tooltips=tooltips)
    p.add_tools(hover)


    p.legend.orientation = "vertical"
    p.legend.label_text_font_size = "10px"
    p.legend.location = "center_right"
    p.legend.click_policy = "hide"


    if nacionalidades_otras:
        label = Label(
            x=0, y=0.55, x_units='data', y_units='data',
            text=f"Otras (<2%): {nacionalidades_otras}",
            text_font_size="11px", text_color="#333", text_align="center"
        )
        p.add_layout(label)


    script, div = components(p)
    resources = CDN.render()
    grafica_html = f"{resources}\n{script}\n{div}"


    return JsonResponse({'grafica_html': grafica_html})

@csrf_exempt
def generar_grafica_lineas(request):
    anio = request.POST.get('anio')
    solo_mortales = request.POST.get('solo_mortales') == 'true'

    if not anio:
        return JsonResponse({'error': 'Debes seleccionar el año.'})

    filtro = {'incidente__fecha__year': anio}
    if solo_mortales:
        filtro['pronostico__nombrepronostico'] = "Ahogamiento mortal"

    qs = (
        Victima.objects
        .filter(**filtro)
        .values('incidente__fecha__month')
        .annotate(Ahogamientos=Count('codvictima'))
        .order_by('incidente__fecha__month')
    )

    df = pd.DataFrame(list(qs))

    if df.empty:
        return JsonResponse({'error': 'No hay datos para esos filtros.'})

    meses = list(range(1,13))
    df = df.set_index('incidente__fecha__month').reindex(meses, fill_value=0).reset_index()
    df.rename(columns={'incidente__fecha__month': 'Mes'}, inplace=True)

    MES_NOMBRES = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                   7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
    df['MesNombre'] = df['Mes'].map(MES_NOMBRES)
    source = ColumnDataSource(df)

    p = figure(
        x_range=df['MesNombre'],
        title=f'Ahogamientos por mes en {anio}',
        x_axis_label='Mes',
        y_axis_label='Número de ahogamientos',
        height=400,
        width=700,
        toolbar_location='right',
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )
    p.line(x='MesNombre', y='Ahogamientos', source=source, line_width=3, color="#1976d2")
    p.circle(x='MesNombre', y='Ahogamientos', size=8, color="#1976d2", source=source)
    hover = HoverTool(
        tooltips=[('Mes', '@MesNombre'), ('Ahogamientos', '@Ahogamientos')],
        mode='vline'
    )
    p.add_tools(hover)
    p.xaxis.major_label_orientation = 1

    script, div = components(p)
    resources = CDN.render()
    return JsonResponse({
        'grafica_html': f"{resources}\n{script}\n{div}"
    })

@csrf_exempt
def generar_diagrama_dispersion(request):
    color_sexo = request.POST.get('color_sexo', 'false') == 'true'
    solo_mortales = request.POST.get('solo_mortales', 'false') == 'true'
    mostrar_linea = request.POST.get('mostrar_linea', 'false') == 'true'

    filtro = {}
    if solo_mortales:
        filtro['pronostico__nombrepronostico'] = "Ahogamiento mortal"

    qs = (
        Victima.objects
        .filter(**filtro)
        .exclude(edad=None)
        .values('edad', 'sexo')
        .annotate(Ahogamientos=Count('codvictima'))
        .order_by('edad')
    )
    df = pd.DataFrame(list(qs))
    if df.empty:
        return JsonResponse({'error': 'No hay datos para esos filtros.'})

    df = df.rename(columns={
        'edad': 'Edad',
        'sexo': 'Sexo',
        'Ahogamientos': 'Ahogamientos'
    })
    df = df[df['Edad'].notnull()]
    df['Edad'] = df['Edad'].astype(int)
    df = df[df['Edad'] >= 0]
    df['Sexo'] = df['Sexo'].astype(str).str.strip().str.title()
    df = df[df['Sexo'].isin(['Hombre', 'Mujer'])]

    if color_sexo:
        df_group = df.groupby(['Edad', 'Sexo'], as_index=False)['Ahogamientos'].sum()
        if df_group.empty:
            return JsonResponse({'error': 'No hay datos de ahogamientos (por sexo) para esos filtros.'})

        sexos_presentes = df_group['Sexo'].unique().tolist()
        colores_dict = {"Hombre": "#1976d2", "Mujer": "#d32f2f"}
        palette = [colores_dict[s] for s in sexos_presentes]
        color_mapper = factor_cmap('Sexo', palette=palette, factors=sexos_presentes)
        legend = 'Sexo'
        hover = HoverTool(tooltips=[
            ('Edad', '@Edad{0}'),
            ('Ahogamientos', '@Ahogamientos{0}')
        ])
    else:
        df_group = df.groupby(['Edad'], as_index=False)['Ahogamientos'].sum()
        if df_group.empty:
            return JsonResponse({'error': 'No hay datos de ahogamientos para esos filtros.'})
        color_mapper = "#1976d2"
        legend = None
        hover = HoverTool(tooltips=[
            ('Edad', '@Edad{0}'),
            ('Ahogamientos', '@Ahogamientos{0}')
        ])

    p = figure(
        height=440,
        width=700,
        title='Diagrama de dispersión de ahogamientos por edad',
        x_axis_label='Edad',
        y_axis_label='Número de ahogamientos',
        tools='pan,wheel_zoom,box_zoom,reset,save',
        toolbar_location='right'
    )

    if not mostrar_linea:
        source = ColumnDataSource(df_group)
        scatter_args = dict(
            x='Edad',
            y='Ahogamientos',
            source=source,
            color=color_mapper,
            size=12,
            alpha=0.8
        )
        if legend:
            scatter_args['legend_field'] = legend
        p.scatter(**scatter_args)

    if mostrar_linea:
        if color_sexo:
            for sexo_valor, color in zip(sexos_presentes, palette):
                sub_df = df_group[df_group['Sexo'] == sexo_valor].sort_values('Edad')
                x = sub_df['Edad'].values
                y = sub_df['Ahogamientos'].values
                x_unique, idx = np.unique(x, return_index=True)
                y_unique = y[idx]
                if len(x_unique) > 3 and np.all(np.diff(x_unique) > 0):
                    x_smooth = np.linspace(x_unique.min(), x_unique.max(), 300)
                    spline = make_interp_spline(x_unique, y_unique, k=3)
                    y_smooth = spline(x_smooth)
                    sub_source = ColumnDataSource({'Edad': x_smooth, 'Ahogamientos': y_smooth})
                    p.line(
                        x='Edad', y='Ahogamientos', source=sub_source,
                        line_width=2, color=color, alpha=0.65, legend_label=f'Tendencia {sexo_valor}'
                    )
                elif len(x_unique) > 1:
                    sub_source = ColumnDataSource({'Edad': x_unique, 'Ahogamientos': y_unique})
                    p.line(
                        x='Edad', y='Ahogamientos', source=sub_source,
                        line_width=2, color=color, alpha=0.65, legend_label=f'Tendencia {sexo_valor}'
                    )
        else:
            x = df_group['Edad'].values
            y = df_group['Ahogamientos'].values
            x_unique, idx = np.unique(x, return_index=True)
            y_unique = y[idx]
            if len(x_unique) > 3 and np.all(np.diff(x_unique) > 0):
                x_smooth = np.linspace(x_unique.min(), x_unique.max(), 300)
                spline = make_interp_spline(x_unique, y_unique, k=3)
                y_smooth = spline(x_smooth)
                source_spline = ColumnDataSource({'Edad': x_smooth, 'Ahogamientos': y_smooth})
                p.line(
                    x='Edad', y='Ahogamientos', source=source_spline,
                    line_width=2, color="#1976d2", alpha=0.65, legend_label="Tendencia"
                )
            elif len(x_unique) > 1:
                p.line(
                    x='Edad', y='Ahogamientos',
                    source=ColumnDataSource({'Edad': x_unique, 'Ahogamientos': y_unique}),
                    line_width=2, color="#1976d2", alpha=0.65, legend_label="Tendencia"
                )

    if (color_sexo and sexos_presentes) or mostrar_linea:
        p.legend.location = "top_right"
        p.legend.label_text_font_size = "10px"
    p.add_tools(hover)

    script, div = components(p)
    resources = CDN.render()
    return JsonResponse({'grafica_html': f"{resources}\n{script}\n{div}"})

@csrf_exempt
def generar_mapa(request):
    solo_mortales = request.POST.get('solo_mortales', 'false') == 'true'
    lugares = request.POST.getlist('lugares[]')

    if not lugares:
        return JsonResponse({'error': 'Debes seleccionar al menos un lugar'})


    gdf = gpd.read_file('C:/Users/Usuario/Desktop/UC/Cuarto_Curso/Segundo Cuatrimestre/TFG/projectAhogamientos/home/data/shapefiles_provincias_espana_actualizado.shp')

    MAPEO_LUGARES = {
        "Playa": ["Playas con vigilancia", "Playas sin vigilancia"],
        "Piscina": [
            "Piscinas domesticas no vigiladas",
            "Piscinas publicas con vigilancia",
            "Piscinas urbanización o privadas no vigiladas",
            "Piscinas de urbanizaciones con vigilancia",
            "Piscinas de equipamientos hoteleros y similares"
        ],
        "Rio": ["Rios, canales y similares"],
        "EmbalsePantano": ["Embalses, Pantanos"],
        "FranjaCosteraAltaMar": ["Franja costera o alta mar"]
    }

    filtro = {}
    if solo_mortales:
        filtro['pronostico__nombrepronostico'] = "Ahogamiento mortal"

    if lugares and "Todos" not in lugares:
        lugares_bd = []
        for lugar in lugares:
            lugares_bd.extend(MAPEO_LUGARES.get(lugar, []))
        filtro['incidente__localizacion__nombrelocalizacion__in'] = lugares_bd

    data = (
        Victima.objects
        .filter(**filtro)
        .values('incidente__localidad__provincia__nombreprovincia')
        .annotate(Ahogamientos=Count('codvictima'))
    )
    df_stats = pd.DataFrame(list(data)).rename(
        columns={'incidente__localidad__provincia__nombreprovincia': 'texto_alt'}
    )

    gdf = gdf.merge(df_stats, on='texto_alt', how='left')
    gdf['Ahogamientos'] = gdf['Ahogamientos'].fillna(0).astype(int)

    geo_source = GeoJSONDataSource(geojson=gdf.to_json())
    palette_red = Reds256[80:][::-1]

    mapper = linear_cmap(
        field_name="Ahogamientos",
        palette=palette_red,
        low=gdf['Ahogamientos'].min(),
        high=gdf['Ahogamientos'].max()
    )

    p = figure(
        title="Ahogamientos por provincia",
        x_axis_location=None, y_axis_location=None,
        width=800, height=600, tools="pan,wheel_zoom,reset,save"
    )
    p.grid.grid_line_color = None

    patches = p.patches(
        'xs', 'ys', source=geo_source,
        fill_color=mapper,
        fill_alpha=0.7, line_color="white", line_width=1
    )

    hover = HoverTool(
        renderers=[patches],
        tooltips=[
            ("Provincia", "@texto_alt"),
            ("Ahogamientos", "@Ahogamientos{0}")
        ]
    )
    p.add_tools(hover)

    color_bar = ColorBar(
        color_mapper=mapper['transform'],
        label_standoff=12,
        width=14,
        location=(0,0),
        ticker=BasicTicker(desired_num_ticks=8),
        formatter=PrintfTickFormatter(format="%d"),
        title="Ahogamientos"
    )
    p.add_layout(color_bar, 'right')

    script, div = components(p)
    resources = CDN.render()
    return JsonResponse({'grafica_html': f"{resources}\n{script}\n{div}"})

@csrf_exempt
def generar_histograma(request):
    solo_mortales = request.POST.get('solo_mortales', 'false') == 'true'
    dias = request.POST.getlist('dias[]')

    if not dias:
        return JsonResponse({'error': 'Debes seleccionar al menos un día.'})
    
    DIAS_NUM = {
        "Lunes": 2,
        "Martes": 3,
        "Miércoles": 4,
        "Jueves": 5,
        "Viernes": 6,
        "Sábado": 7,
        "Domingo": 1
    }

    if "Todos" in dias:
        dias_django = list(DIAS_NUM.values())
    else:
        try:
            dias_django = [DIAS_NUM[d] for d in dias]
        except KeyError:
            return JsonResponse({'error': 'Día de la semana no válido.'})

    filtro = {}
    if solo_mortales:
        filtro['pronostico__nombrepronostico'] = "Ahogamiento mortal"

    qs = (
        Victima.objects
        .filter(**filtro)
        .exclude(incidente__hora=None)
        .exclude(incidente__fecha=None)
        .annotate(
            dia_semana=ExtractWeekDay('incidente__fecha')
        )
        .filter(dia_semana__in=dias_django)
    )

    registros = []
    for v in qs:
        if v.incidente.hora:
            registros.append(v.incidente.hora.hour)

    df_registros = pd.DataFrame(registros, columns=['hora'])
    conteo = df_registros['hora'].value_counts().sort_index()

    todas_horas = pd.Series(0, index=range(24))
    todas_horas.update(conteo)

    df_final = pd.DataFrame({
        'hora': todas_horas.index,
        'Ahogamientos': todas_horas.values
    })

    intervalos = [f"{h}-{(h+1)%24}" for h in range(24)]
    df_final['hora_label'] = intervalos

    source = ColumnDataSource(df_final)
    p = figure(
        x_range=intervalos,
        height=400,
        width=800,
        title="Ahogamientos por hora del día",
        x_axis_label='Intervalo horario',
        y_axis_label='Número de ahogamientos',
        toolbar_location='above',
        tools='pan,wheel_zoom,reset,save'
    )
    p.vbar(
        x='hora_label',
        top='Ahogamientos',
        width=0.92,
        source=source,
        fill_color="#d32f2f",
        line_color="#d32f2f",
        alpha=0.85
    )

    hover = HoverTool(tooltips=[
        ("Intervalo de horas", "@hora_label"),
        ("Ahogamientos", "@Ahogamientos{0}")
    ])
    p.add_tools(hover)
    p.xaxis.major_label_orientation = 1

    script, div = components(p)
    resources = CDN.render()
    return JsonResponse({'grafica_html': f"{resources}\n{script}\n{div}"})

@csrf_exempt
def generar_radar(request):
    filtro = request.POST.get('filtro')

    MAPEO_FILTROS = {
        "actividad": "incidente__actividad__nombreactividad",
        "deteccion": "incidente__deteccion__nombredeteccion",
        "riesgo": "incidente__riesgo__nombreriesgo",
        "localizacion": "incidente__localizacion__nombrelocalizacion",
        "intervencion": "incidente__intervencion__nombreintervencion",
        "zonavigilada": "incidente__zona__nombrezonavigilada",
        "causa": "causavictima__causa__nombrecausa",
        "factorriesgo": "factorriesgovictima__factorriesgo__nombrefactorriesgo",
        "antecedente": "antecedentevictima__antecedente__nombreantecedente",
        "primerinterviniente": "primerinterviniente__nombreprimerinterviniente",
        "materialrescate": "materialrescate__nombrematerialrescate",
        "extraccion": "extraccion__nombreextraccion",
        "tipoahogamiento": "tipoahogamiento__nombretipoahogamiento",
        "reanimacion": "reanimacion__nombrereanimacion",
        "pronostico": "pronostico__nombrepronostico"
    }

    TITULO_FILTROS = {
        "actividad": "actividad",
        "deteccion": "detección",
        "riesgo": "riesgo detectado",
        "localizacion": "localización",
        "intervencion": "intervención",
        "zonavigilada": "zona vigilada",
        "causa": "causa del ahogamiento",
        "factorriesgo": "factor de riesgo",
        "antecedente": "antecedente",
        "primerinterviniente": "primer interviniente",
        "materialrescate": "material de rescate",
        "extraccion": "extracción",
        "tipoahogamiento": "ahogamiento",
        "reanimacion": "reanimación",
        "pronostico": "pronóstico"
    }

    if not filtro or filtro not in MAPEO_FILTROS:
        return JsonResponse({'error': 'Debes seleccionar un filtro válido.'})

    campo_bd = MAPEO_FILTROS[filtro]

    data = (
        Victima.objects
        .values(campo_bd)
        .annotate(num=Count('codvictima'))
    )
    df = pd.DataFrame(list(data))
    if df.empty:
        return JsonResponse({'error': 'No hay datos para este filtro.'})

    categoria = campo_bd.split('__')[-1]
    df[campo_bd] = df[campo_bd].fillna('Desconocido').astype(str)

    df = df[~df[campo_bd].str.strip().str.lower().isin(['sin datos', 'desconocido', 'n/a', 'nan', 'no consta', '-', 'none'])]
    df = df.sort_values('num', ascending=False).head(7)

    categorias = df[campo_bd].tolist()
    valores = df['num'].tolist()

    if len(categorias) < 3:
        return JsonResponse({'error': 'Hace falta mínimo 3 categorías para hacer radar.'})

    N = len(categorias)
    angle_offset = np.pi/2
    angles = np.linspace(0, 2*np.pi, N, endpoint=False) - angle_offset
    angles_poly = np.concatenate([angles, [angles[0]]])

    canvas_size = 750
    max_radio = max(valores) * 1.08
    x_poly = max_radio * np.cos(angles_poly)
    y_poly = max_radio * np.sin(angles_poly)
    x = np.array(valores) * np.cos(angles)
    y = np.array(valores) * np.sin(angles)
    x_data = np.concatenate([x, [x[0]]])
    y_data = np.concatenate([y, [y[0]]])

    x_label = max_radio * 1.08 * np.cos(angles)
    y_label = max_radio * 1.08 * np.sin(angles)
    x_val = (np.array(valores) + max_radio*0.05) * np.cos(angles)
    y_val = (np.array(valores) + max_radio*0.05) * np.sin(angles)

    source_poly = ColumnDataSource(dict(
        x_data=x_data,
        y_data=y_data
    ))

    source_labels = ColumnDataSource(dict(
        x=x,
        y=y,
        x_label=x_label,
        y_label=y_label,
        x_val=x_val,
        y_val=y_val,
        cat=categorias,
        val=[str(v) for v in valores]
    ))



    titulo = TITULO_FILTROS.get(filtro, filtro.capitalize())

    p = figure(
        title=f"Ahogamientos por tipo de {titulo}",
        width=canvas_size, height=canvas_size,
        x_axis_type=None, y_axis_type=None,
        x_range=(-max_radio*1.5, max_radio*1.5), y_range=(-max_radio*1.5, max_radio*1.5)
    )
    p.grid.grid_line_color = None
    p.outline_line_color = None

    p.patch(x_poly, y_poly, color="#ececec", alpha=0.7, line_width=2)

    for i in range(N):
        p.line([0, x_poly[i]], [0, y_poly[i]], color="#bbb", line_dash="dotted", line_width=1.2)

    p.line('x_data', 'y_data', source=source_poly, color="#1976d2", line_width=3)
    p.patch('x_data', 'y_data', source=source_poly, color="#1976d2", alpha=0.16)

    # Puntos y etiquetas con source_labels
    p.scatter('x', 'y', source=source_labels, marker="circle", size=16, color="#d32f2f")

    p.add_layout(LabelSet(
        x='x_label', y='y_label', text='cat', source=source_labels,
        text_align='center', text_font_size='12px', text_font_style='bold',
        background_fill_color='white', background_fill_alpha=0.92
    ))
    p.add_layout(LabelSet(
        x='x_val', y='y_val', text='val', source=source_labels,
        text_align='center', text_font_size='10px', text_color="#1976d2",
        background_fill_color='white', background_fill_alpha=0.78
    ))

    script, div = components(p)
    resources = CDN.render()
    return JsonResponse({'grafica_html': f"{resources}\n{script}\n{div}"})

@csrf_exempt
def comparativa_sklearn(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido.'})

    try:
        actividad = request.POST.get('actividad', '').strip()
        localizacion = request.POST.get('localizacion', '').strip()
        zonavigilada = request.POST.get('zonavigilada', '').strip()
        factorriesgo = request.POST.get('factorriesgo', '').strip()
        intervencion = request.POST.get('intervencion', '').strip()
        edad = request.POST.get('edad', '').strip()
        edad = int(edad) if edad else None

        if (not actividad and not localizacion and not zonavigilada and not factorriesgo and not intervencion and not edad):
            return JsonResponse({'error': 'Debes introducir al menos un filtro o la edad.'})

        qs = Victima.objects.values(
            'incidente__actividad__nombreactividad',
            'incidente__localizacion__nombrelocalizacion',
            'incidente__zona__nombrezonavigilada',
            'factorriesgovictima__factorriesgo__nombrefactorriesgo',
            'incidente__intervencion__nombreintervencion',
            'edad',
            'pronostico__nombrepronostico'
        )
        df = pd.DataFrame(list(qs))

        col_map = {
            'actividad': 'incidente__actividad__nombreactividad',
            'localizacion': 'incidente__localizacion__nombrelocalizacion',
            'zonavigilada': 'incidente__zona__nombrezonavigilada',
            'factorriesgo': 'factorriesgovictima__factorriesgo__nombrefactorriesgo',
            'intervencion': 'incidente__intervencion__nombreintervencion',
            'edad': 'edad'
        }
        columnas_clave = list(col_map.values()) + ['pronostico__nombrepronostico']
        df = df.dropna(subset=columnas_clave)
        valores_invalidos = ['sin datos', 'desconocido', 'n/a', 'nan', '', 'no consta', '-', 'none']
        for col in columnas_clave:
            if df[col].dtype == 'O':
                df = df[~df[col].str.strip().str.lower().isin(valores_invalidos)]
        df = df[pd.to_numeric(df['edad'], errors='coerce').notnull()]
        df['edad'] = df['edad'].astype(float)
        max_puntos = 1000
        if len(df) > max_puntos:
            df = df.sample(n=max_puntos, random_state=42)
        df = df.reset_index(drop=True)
        df['mortal'] = (df['pronostico__nombrepronostico'].str.strip().str.lower() == "ahogamiento mortal").astype(int)
        y = df['mortal']

        cat_cols = [
            'incidente__actividad__nombreactividad',
            'incidente__localizacion__nombrelocalizacion',
            'incidente__zona__nombrezonavigilada',
            'factorriesgovictima__factorriesgo__nombrefactorriesgo',
            'incidente__intervencion__nombreintervencion'
        ]
        num_cols = ['edad']
        def valor_default(col):
            if col in cat_cols:
                return df[col].mode().iloc[0] if not df[col].mode().empty else ''
            if col == 'edad':
                return float(df['edad'].median())
            return ''
        nuevo_dict = {
            'incidente__actividad__nombreactividad': actividad or valor_default('incidente__actividad__nombreactividad'),
            'incidente__localizacion__nombrelocalizacion': localizacion or valor_default('incidente__localizacion__nombrelocalizacion'),
            'incidente__zona__nombrezonavigilada': zonavigilada or valor_default('incidente__zona__nombrezonavigilada'),
            'factorriesgovictima__factorriesgo__nombrefactorriesgo': factorriesgo or valor_default('factorriesgovictima__factorriesgo__nombrefactorriesgo'),
            'incidente__intervencion__nombreintervencion': intervencion or valor_default('incidente__intervencion__nombreintervencion'),
            'edad': edad if edad is not None else valor_default('edad')
        }
        nuevo_caso = pd.DataFrame([nuevo_dict])

        df_X = df[cat_cols + num_cols]
        X_concat = pd.concat([df_X, nuevo_caso], ignore_index=True)
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        cat_encoded = encoder.fit_transform(X_concat[cat_cols])
        scaler = StandardScaler()
        edad_scaled = scaler.fit_transform(X_concat[['edad']])
        X_total = np.hstack([cat_encoded, edad_scaled])

        X_model = X_total[:-1, :]
        X_caso = X_total[-1, :].reshape(1, -1)
        model = RandomForestClassifier(n_estimators=80, random_state=7)
        model.fit(X_model, y)
        prob_mortal = model.predict_proba(X_caso)[0, 1]

        texto_prob = (
            f"⚠️ Probabilidad estimada de <b>mortalidad</b>: "
            f"<b>{prob_mortal*100:.1f}%</b> "
            f"<br><span style='font-size:12px;'>(por modelo predictivo usando todas las variables seleccionadas)</span>"
        )

        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X_total)
        idx_nuevo = len(X_2d) - 1

        df_hist = pd.DataFrame({
            'x': X_2d[:-1, 0],
            'y': X_2d[:-1, 1],
            'actividad': df['incidente__actividad__nombreactividad'],
            'localizacion': df['incidente__localizacion__nombrelocalizacion'],
            'factorriesgo': df['factorriesgovictima__factorriesgo__nombrefactorriesgo'],
            'color': df['mortal'].map({0: '#1976d2', 1: '#d32f2f'})
        })
        source_hist = ColumnDataSource(df_hist)
        df_user = pd.DataFrame([{
            'x': X_2d[-1, 0],
            'y': X_2d[-1, 1],
            'color': 'orange'
        }])
        source_user = ColumnDataSource(df_user)

        p = figure(
            title="Comparativa del caso introducido con datos históricos",
            width=650, height=500,
            tools="pan,wheel_zoom,box_zoom,reset,save",
            active_scroll="wheel_zoom",
            background_fill_color="#fafafa"
        )

        p.xaxis.visible = False
        p.yaxis.visible = False
        p.grid.grid_line_color = None

        scatter_hist = p.scatter(
            'x', 'y', color='color', size=8, alpha=0.63,
            source=source_hist
        )

        p.scatter(
            'x', 'y', color='color', size=18, marker='star',
            source=source_user
        )

        hover = HoverTool(
            tooltips=[
                ("Actividad", "@actividad"),
                ("Localización", "@localizacion"),
                ("Factor riesgo", "@factorriesgo")
            ],
            renderers=[scatter_hist]
        )
        p.add_tools(hover)

        script, div = components(p)
        resources = CDN.render()
        grafica_html = f"{resources}\n<div style='margin-bottom:13px; font-size:18px; color:#b62c2c; letter-spacing:-0.5px;'>{texto_prob}</div>{script}\n{div}"

        return JsonResponse({'grafica_html': grafica_html})

    except Exception as e:
        return JsonResponse({'error': f'Error en procesamiento: {str(e)}'})
    
@csrf_exempt
def generar_mapa_hotspots(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'})

    anio_inicio = request.POST.get('anio-inicio-hotspots')
    anio_fin = request.POST.get('anio-fin-hotspots')

    if not anio_inicio and not anio_fin:
        return JsonResponse({'error': 'Introduce un rango de años'})
    
    if anio_fin < anio_inicio:
        return JsonResponse({'error': 'El año de fin no puede ser inferior al de inicio'})

    try:
        anio_inicio = int(anio_inicio) if anio_inicio else 2000
        anio_fin = int(anio_fin) if anio_fin else datetime.now().year
    except:
        return JsonResponse({'error': 'Valores inválidos para años'})

    qs = Victima.objects.filter(
        incidente__fecha__year__gte=anio_inicio,
        incidente__fecha__year__lte=anio_fin
    ).values(
        'codvictima',
        'incidente__fecha',
        'incidente__latitud',
        'incidente__longitud',
        'pronostico__nombrepronostico',
        'incidente__localidad__nombrelocalidad'
    )

    df = pd.DataFrame(list(qs))

    if df.empty:
        return JsonResponse({'error': 'No hay datos para ese rango'})

    df['incidente__latitud'] = pd.to_numeric(df['incidente__latitud'], errors='coerce')
    df['incidente__longitud'] = pd.to_numeric(df['incidente__longitud'], errors='coerce')
    df = df.dropna(subset=['incidente__latitud', 'incidente__longitud'])
    df['incidente__fecha'] = pd.to_datetime(df['incidente__fecha'])
    df['month'] = df['incidente__fecha'].dt.strftime('%B')
    df['victims'] = 1  
    df['mortal'] = df['pronostico__nombrepronostico'].str.strip().str.lower().eq('ahogamiento mortal').astype(int)

    coords = df[['incidente__latitud', 'incidente__longitud']].to_numpy()
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords)

    dbscan = DBSCAN(eps=0.01, min_samples=3) 
    labels = dbscan.fit_predict(coords_scaled)
    df['cluster'] = labels

    df = df[df['cluster'] != -1]

    if df.empty:
        return JsonResponse({'error': 'No se detectaron hotspots (clusters) con los parámetros elegidos.'})

    summary = df.groupby('cluster').agg(
        total_incidents=('codvictima', 'count'),
        total_victims=('victims', 'sum'),
        total_mortal=('mortal', 'sum'),
        most_common_month=('month', lambda x: x.mode().iloc[0] if not x.mode().empty else ''),
        main_place=('incidente__localidad__nombrelocalidad', lambda x: x.mode().iloc[0] if not x.mode().empty else 'Desconocido') 
    ).reset_index()

    summary['mortality_rate'] = (summary['total_mortal'] / summary['total_incidents'] * 100).round(1)
    summary = summary.sort_values(by='total_incidents', ascending=False).reset_index(drop=True)

    centers = []
    for cluster in summary['cluster']:
        points = df[df['cluster'] == cluster][['incidente__latitud','incidente__longitud']]
        center = points.mean().to_list()
        centers.append(center)
    summary['center_lat'] = [c[0] for c in centers]
    summary['center_lon'] = [c[1] for c in centers]

    map_div = '<div id="mapa-hotspots" style="height: 400px; margin-top: 10px;"></div>'
    html_response = f'<div><h3>Hotspots Detectados con Clustering Espacial</h3>{map_div}</div>'

    return JsonResponse({'html': html_response, 'clusters': summary.to_dict(orient="records")})


