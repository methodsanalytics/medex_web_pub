from django.conf.urls import url
from django.urls import include, path

from home import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login', views.login, name='login'),
  path('login-callback', views.login_callback, name='login_callback'),
  path('logout', views.logout, name='logout'),
  path('forgotten-password', views.forgotten_password, name='forgotten-password'),
  path('reset-sent', views.reset_sent, name='reset-sent'),
  path('settings', views.settings_index, name='settings_index'),
  url(r'^users/', include('users.urls')),
  url(r'^cases/', include('examinations.urls')),
]
