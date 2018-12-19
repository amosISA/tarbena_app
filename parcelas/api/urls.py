from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^fullparcelas/$',
         views.ParcelasListView.as_view(),
         name='parcelas_list'),

    url(r'^parcelasbysector/(?P<pk>\d+)/$',
         views.ParcelasBySectorView.as_view(),
         name='parcelas_by_sector'),

    url('^getparcelassector/(?P<sector>.+)/$', views.GetParcelasBySector.as_view()),
]