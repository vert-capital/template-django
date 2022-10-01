import django_cas_ng.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token

from .cas_wrapper import APILoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/user/login", obtain_jwt_token),
    path("accounts/login", APILoginView.as_view(), name="cas_ng_login"),
    path("accounts/login/", APILoginView.as_view()),
    path(
        "accounts/logout",
        django_cas_ng.views.LogoutView.as_view(),
        name="cas_ng_logout",
    ),
    path("", include("apps.user.urls")),
    path("", include("apps.main.urls")),
]

if settings.LOCAL_ENV:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
