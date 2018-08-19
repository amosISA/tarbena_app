from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^holidays/$',
         views.HolidayListView.as_view(),
         name='holiday_list'),
     url(r'^holidays/(?P<pk>\d+)/$',
         views.HolidayDetailView.as_view(),
         name='holiday_detail'),
]