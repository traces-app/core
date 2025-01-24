from django.urls import include, path

urlpatterns = [
    path('status/', include('api.urls.status_urls')),  # Link to status URL:
]