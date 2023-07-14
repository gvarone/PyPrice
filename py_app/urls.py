from django.urls import path
from py_app import views

app_name = 'py_app'

urlpatterns = [
    path('', views.base, name='base'),
    path('help', views.help, name='help'),
    path('register', views.register, name='register'),
    path('user_login', views.user_login, name='user_login'),
]