"""tarbena URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth import views as auth_views

from . import views
from profiles.views import activate_user_view


urlpatterns = [
    # Admin
    url(r'^panel/docs/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    url(r'^panel/', admin.site.urls),

    #url(r'^profile/', include('profiles.urls', namespace='profiles')),
    url(r'^subvenciones/', include('subvenciones.urls', namespace='subvenciones')),

    # Entry point to main app: Index
    url(r'^$', views.index, name='index'),

    # Login, Register, Activation email, reset, confirm Password
    url(r'^login/$', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^logout/', logout, {'next_page': '/login/'}, name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    #url('^change-password/$', auth_views.password_change, {'post_change_redirect' : '/'}, name='password_change'),
    url(r'^reset/password_reset', password_reset, {"template_name": "registration/password_reset_form.html",
        "email_template_name": "registration/password_reset_email.html"}, name="password_reset"),
    url(r'^password_reset_done', password_reset_done, {"template_name":"registration/password_reset_done.html"},
        name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete, {'template_name': 'registration/password_reset_complete.html'},
        name='password_reset_complete'),

    # Markdown editor for user mentions and notifications
    url(r'^martor/', include('martor.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

