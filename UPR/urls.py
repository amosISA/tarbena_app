from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_maquinas, name='index'),
    url(r'^maquina/(?P<ninventario>[-\w\d]+)/$', views.maquina_detail, name='maquina_detail'),
    url(r'^incidencia/(?P<ninventario>[-\w\d]+)/$', views.add_incicencia, name='add_incidencia'),
]