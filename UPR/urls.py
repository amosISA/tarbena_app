from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_maquinas, name='index'),
    url(r'^maquina/(?P<ninventario>[-\w\d]+)/$', views.maquina_detail, name='maquina_detail'),
    url(r'^incidencia/(?P<ninventario>[-\w\d]+)/$', views.add_incidencia, name='add_incidencia'),
    url(r'^ajaxgetcomponentsbygroup/$', views.get_components_by_group, name='get_components_by_group'),
    url(r'^ubicacion/(?P<ninventario>[-\w\d]+)/$', views.add_ubicacion, name='add_ubicacion'),
    url(r'^obra/(?P<ninventario>[-\w\d]+)/$', views.add_obra, name='add_obra'),
    url('ultimasincidencias/', views.ultimas_incidencias, name='ultimas_incidencias'),
    url('protectorcuchilla/', views.protector_cuchilla, name='protector_cuchilla'),
    url(r'^componente/(?P<ncomponente>[-\w\d]+)/$', views.componente_detail, name='componente_detail'),
]