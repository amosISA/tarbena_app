from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajaxsectores/$', views.ajax_get_sectores, name='ajax_get_sectores'),
    url(r'^ajaxproyectos/$', views.ajax_get_projects, name='ajax_get_proyectos'),
    url(r'^ajaxparcelas/$', views.ajax_get_parcelas, name='ajax_get_parcelas'),
]