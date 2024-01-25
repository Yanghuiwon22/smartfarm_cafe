from .models import CustomUser
from django.contrib import admin

# Register your models here.
class set_table(admin.ModelAdmin):
    list_display = ('username', 'student_number','name', 'is_superuser')
admin.site.register(CustomUser, set_table)
