from django.contrib import admin
from .models import Message, ReserveMealMessage, BookstoreMessage
# Register your models here.
# admin.site.register(Message)
admin.site.register(ReserveMealMessage)
admin.site.register(BookstoreMessage)
