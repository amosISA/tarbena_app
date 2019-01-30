from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajaxsectores/$', views.ajax_get_sectores, name='ajax_get_sectores'),
    url(r'^ajaxproyectos/$', views.ajax_get_projects, name='ajax_get_proyectos'),
    url(r'^ajaxparcelas/$', views.ajax_get_parcelas, name='ajax_get_parcelas'),
    url(r'^ajaxm2/$', views.get_m2_url, name='ajax_get_m2'),
    url(r'^ajaxparcelainfo/$', views.get_parcela_info_url, name='ajax_get_parcela_info'),
    # url(r'^detail_propietario/(?P<pk>.+)/$', views.DetailPropietarioParcela.as_view(), name="detail_propietario"),
    url(r'^add/$', views.ParcelaCreate, name="add_parcela"),
    url(r'^propietario-autocomplete/$', views.PropietarioAutocomplete.as_view(), name='propietario-autocomplete'),
    url(r'^autorizacion/(?P<parcela_id>\d+)/pdf/$',
            views.autorization_pdf_maker,
            name='get_autorizacion'),
    url(r'^propietario/getparcelas/$',
            views.get_propietario_parcelas,
            name='get_propietario_parcelas'),
]