from django.contrib import admin
# from api.models import User
from .models import user

# Register your models here.
admin.site.register(user.User)
admin.site.register(user.Role)
