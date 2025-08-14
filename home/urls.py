from django.urls import path
from . import views

urlpatterns = [
    path('generar_grafica_apilada/', views.generar_grafica_apilada, name='generar_grafica_apilada'),
    path('generar_grafica_circular/', views.generar_grafica_circular, name='generar_grafica_circular'),
    path('generar_grafica_lineas/', views.generar_grafica_lineas, name='generar_grafica_lineas'),
    path('generar_diagrama_dispersion/', views.generar_diagrama_dispersion, name='generar_diagrama_dispersion'),
    path('generar_mapa/', views.generar_mapa, name='generar_mapa'),
    path('generar_histograma/', views.generar_histograma, name='generar_histograma'),
    path('generar_radar/', views.generar_radar, name='generar_radar'),
    path('comparativa_sklearn/', views.comparativa_sklearn, name='comparativa_sklearn'),
    path('generar_mapa_hotspots/', views.generar_mapa_hotspots, name='generar_mapa_hotspots'),
    path('generar_kmeans/', views.generar_kmeans, name='generar_kmeans'),
    path('generar_tree/', views.generar_tree, name='generar_tree'),
    path('', views.home),
]
