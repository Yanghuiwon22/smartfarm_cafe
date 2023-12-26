from django.contrib import admin
from .models import BookStore, Category
# Register your models here.
admin.site.register(BookStore)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_field = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)