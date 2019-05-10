from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_maquinas, name='index'),
    url(r'^catalog/(?P<id>\d+)/$', views.maquina_detail, name='maquina_detail'),
]
