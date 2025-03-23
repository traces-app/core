from django.urls import include, path

urlpatterns = [
    path('status/', include('api.urls.status_urls')),
    path('auth/', include('api.urls.auth_urls')),  
    path('user/', include('api.urls.user_urls')),  
]