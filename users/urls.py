from django.urls import path
#using Django Token Authentication without JWT
from rest_framework.authtoken import views

from .views import RegisterView, UserView, LoginView, UserViewDetail

urlpatterns = [
    path("users/register/", RegisterView.as_view()),
    path("users/", UserView.as_view()),
    path("users/<int:user_id>/", UserViewDetail.as_view()),
    path("token-auth", views.obtain_auth_token),
    path("users/login/", LoginView.as_view()),
]


# To use jwt:

# from rest_framework_simplejwt import views

# path("users/login/", views.TokenObtainPairView.as_view()),
# path("token/refresh/", views.TokenRefreshView.as_view()),