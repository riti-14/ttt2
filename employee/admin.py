

from django.contrib import admin
from .models import empleave_model
# ,empregister_model,status_model
from .models import myuser_model
from django.contrib.auth.admin import UserAdmin


# Register your models here.
# admin.site.register(empregister_model)  
admin.site.register(empleave_model)
# admin.site.register(status_model)

admin.site.register(myuser_model,UserAdmin)




UserAdmin.fieldsets += ("Add fields:",{'fields':('status',)} ),

