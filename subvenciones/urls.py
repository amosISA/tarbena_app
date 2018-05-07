from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_subvenciones, name='index'),
    url(r'^(?P<estado_slug>[-\w ]+)/$', views.index_subvenciones, name='subvencion_by_category'),
]