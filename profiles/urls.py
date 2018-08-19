from django.conf.urls import url

from .views import ProfileDetailView, upload_avatar , ProfileUpdateView

urlpatterns = [
    url(r'^configuration/', ProfileUpdateView.as_view(), name='update_profile'),
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='user_profile'),
    url(r'^upload/avatar/$', upload_avatar, name='upload_avatar'),
]