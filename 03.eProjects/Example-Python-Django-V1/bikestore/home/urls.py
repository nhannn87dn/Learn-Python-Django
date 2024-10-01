from django.urls import path

from . import views

# Khai báo url cho view ở bên file view
urlpatterns = [
    path("", views.index, name="home_index"),
    path("sendmail/", views.sendmail, name="home_sendmail"),
]