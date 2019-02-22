from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_museo, name='index'),
    url(r'^catalog/(?P<id>\d+)/$', views.museo_detail, name='museu_detail'),
]