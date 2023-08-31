from django.urls import path

from .views import registerUser, loginUser, updateUser, getUser

app_name = 'authC'
urlpatterns = [
    path('reg/', registerUser, name='registration'),
    path('login/', loginUser, name='login'),
    path('', getUser, name='get user'),
    path('', updateUser, name='update user'),
]