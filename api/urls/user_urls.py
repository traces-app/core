from django.urls import path
from api.views.fcm_token_view import FCMTokenView

urlpatterns = [
    path('fcm-token/', FCMTokenView.as_view(), name='fcm_token_actions'),
]