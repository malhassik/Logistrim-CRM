from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.truck_list, name="truck_list"),
    path("upload/", views.upload_document, name="upload_document"),
    path("fuel/", views.fuel_list, name="fuel_list"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="fleet/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/login/"), name="logout"),
]
