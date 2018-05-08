from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.SubvencionCreateView.as_view(), name='create'),
    url(r'^ajax/load-areas/$', views.load_areas, name='ajax_load_areas'),
    url(r'^$', views.index_subvenciones, name='index'),
    url(r'^(?P<estado_slug>[-\w ]+)/$', views.index_subvenciones, name='subvencion_by_category'),
]