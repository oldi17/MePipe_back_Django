from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('auth/', include('authC.urls', namespace='authC')),
    path('api/creator/', include('creator.urls', namespace='creator')),
    path('api/v/', include('video.urls', namespace='video')),
]
