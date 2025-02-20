from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from api.views.auth_view import Authenticate, CreateUserView, UserInfoView

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_information'),
    path('login/', Authenticate.as_view(), name='token_obtain_pair'),
    path('register/', CreateUserView.as_view(), name='create_new_user'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]