from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("truck/<int:truck_id>/", views.truck_detail, name="truck_detail"),
    path("triplog/", views.trip_log, name="trip_log"),
    path("driver/<int:driver_id>/", views.driver_detail, name="driver_detail"),
    path(
        "upload/<int:truck_id>/",
        views.upload_document,
        name="upload_document_for_truck",
    ),
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
    path(
        "truck/<int:truck_id>/fuel/add/",
        views.add_fuel_records,
        name="add_fuel_record_for_truck",
    ),
    path(
        "api/trucks/<int:pk>/",
        views.TruckDetailAPIView.as_view(),
        name="api_truck_detail",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
