from django.urls import path

from .views import logoutUser, registerUser, loginUser, updateUser, getUser

app_name = 'authC'
urlpatterns = [
    path('reg/', registerUser, name='registration'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('', getUser, name='get user'),
    path('', updateUser, name='update user'),
]