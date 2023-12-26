# from django.contrib import admin
# from .models import Archive
#
# admin.site.register(Archive)

from django.contrib import admin
from .models import Archive

admin.site.register(Archive)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_field = {'slug': ('name',)}

# admin.site.register(Category, CategoryAdmin)