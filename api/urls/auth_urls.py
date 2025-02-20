from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from api.views.auth_view import Authenticate, CreateUserView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='create_new_user'),
    path('login/', Authenticate.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]