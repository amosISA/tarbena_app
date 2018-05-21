from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ajaxareas/$', views.subsidies_for_ajax_loop, name='ajax_loop_areas'),
    url(r'^ajaxrelation/$', views.ajax_se_relaciona_con, name='ajax_se_relaciona_con'),
    url(r'^like/$', views.likes, name='like'),
    url(r'^favourites/$', views.favourites, name='favourites'),
    url(r'^new/$', views.SubvencionCreateView.as_view(), name='create'),
    url(r'^$', views.index_subvenciones, name='index'),
    url(r'^edit/(?P<pk>[\w-]+)/$', views.SubvencionUpdateView.as_view(), name='edit_subvencion'),
    url(r'^delete/(?P<pk>[\w-]+)/$', views.SubvencionDeleteView.as_view(), name='delete_subvencion'),
    url(r'^(?P<id>\d+)/$', views.subvencion_detail, name='subvencion_detail'),
    url(r'^(?P<estado_slug>[-\w ]+)/$', views.index_subvenciones, name='subvencion_by_category'),
]