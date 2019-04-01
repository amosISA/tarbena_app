from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_facturas, name='index'),
    url(r'^api/data/$', views.get_data, name='api-data'),
    url(r'^api/contador/total/consumo/$', views.ContadoresTotalConsumo.as_view()),
    url(r'^api/contador/consumo/(?P<contador_id>\d+)/$', views.totalConsumoByContador, name='api-consumo-by-contador'),
]