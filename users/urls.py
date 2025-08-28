from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views

urlpatterns = [
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("profile/update/", views.UserProfileUpdateAPIView.as_view(), name="update"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]