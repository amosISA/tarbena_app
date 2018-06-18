from django.conf.urls import url

from .views import ProfileDetailView, upload_avatar

urlpatterns = [
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='user_profile'),
    url(r'^upload/avatar/$', upload_avatar, name='upload_avatar'),
]