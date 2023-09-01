from django.urls import path

from .views import registerUser, loginUser, modifyUser, getUser

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'authC'
urlpatterns = [
    path('reg/', registerUser, name='register'),
    path('login/', loginUser, name='login'),
    path('api/token/', loginUser, name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', getUser, name='get'),
    path('modify/', modifyUser, name='modify'),
]