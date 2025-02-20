from django.contrib import admin
# from api.models import User
from .models import user

# Register your models here.
admin.site.register(user.User)
admin.site.register(user.StandardUser)
admin.site.register(user.MerchantAdministrator)
admin.site.register(user.LogisticsAdministrator)
admin.site.register(user.Driver)
