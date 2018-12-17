from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

# from rest_framework.routers import DefaultRouter
from drf_auto_endpoint.router import router
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .users.views import UserViewSet, UserCreateViewSet
from applyonline.views import home, GoogleLogin, GoogleConnect
from allauth.account.views import ConfirmEmailView

# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'users', UserCreateViewSet)

router.registerViewSet(r"users", UserViewSet)
router.registerViewSet(r"users", UserCreateViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    # path('api-token-auth/', views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    # re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
    re_path(r"^$", home),
    path(r"api-token-auth/", obtain_jwt_token),
    path(r"api-token-refresh/", refresh_jwt_token),
    path("accounts/", include("allauth.urls")),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("rest-auth/google/connect/", GoogleConnect.as_view(), name="google_connect"),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
