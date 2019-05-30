from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_maquinas, name='index'),
    url(r'^maquina/(?P<ninventario>[-\w\d]+)/$', views.maquina_detail, name='maquina_detail'),
    url(r'^incidencia/(?P<ninventario>[-\w\d]+)/$', views.add_incidencia, name='add_incidencia'),
    url(r'^ajaxgetcomponentsbygroup/$', views.get_components_by_group, name='get_components_by_group'),
    #url(r'^incidencia/new/$', views.NewMaquinaIncidencia.as_view(), name='create_maquina_incidencia'),
]