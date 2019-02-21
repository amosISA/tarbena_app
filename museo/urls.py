from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_museo, name='index'),
    #museu/catalog/id => para la ficha
]