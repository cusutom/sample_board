from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('welcome', views.welcome, name='welcome'),
    path('new_regist', views.new_regist, name='new_regist'),
    path('home', views.home, name='home'),
    path('regist', views.regist, name='regist'),
    path('login', views.login_user, name='login'),
    path('edit', views.edit_user, name='edit'),
    path('delete/<int:id>', views.delete_user, name='delete'),
    path('logout', views.logout_user, name='logout'),
    path('welcome', views.home, name='welcome'), 
]