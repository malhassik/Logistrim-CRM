from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.block_truck_list, name="block_truck_list"),
    path(
        "upload/<int:truck_id>/",
        views.upload_document,
        name="upload_document_for_truck",
    ),
    path("fuel/", views.fuel_list, name="fuel_list"),
    path("api/trucks/", views.TruckListAPIView.as_view(), name="api_truck_list"),
    path(
        "api/trucks/<int:pk>/",
        views.TruckDetailAPIView.as_view(),
        name="api_truck_detail",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="fleet/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/login/"), name="logout"),
    path("fuel/add/", views.add_fuel_records, name="add_fuel_record"),
    path("truck/add/", views.add_truck, name="add_truck"),
    path("driver/add/", views.add_driver, name="add_driver"),
    path("truck/<int:truck_id>/edit/", views.edit_truck, name="edit_truck"),
    path("truck/<int:truck_id>/delete", views.delete_truck, name="delete_truck"),
    path(
        "api/trucks/<int:pk>/",
        views.TruckDetailAPIView.as_view(),
        name="api_truck_detail",
    ),
    path(
        "truck/<int:truck_id>/", views.truck_detail, name="truck_detail"
    ),  # <--- НОВЫЙ ПУТЬ
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
