from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.contrib import admin
from api.views import *

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'admusers', AdminUserViewSet, basename='admuser')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'admsessions', AdminSessionViewSet, basename='admsession')
router.register(r'fixed_sessions', FixedSessionViewSet, basename='fixed_session')
router.register(r'ddates', DisabledDateViewSet, basename='ddate')
router.register(r'reschedules', ReschedulesViewSet, basename='reschedules')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]