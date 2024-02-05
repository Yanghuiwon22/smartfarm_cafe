from django.db import models
from django.contrib.auth.models import User
from itertools import chain
from softeng_2023_prj import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # anonymous = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"From {self.sender} to {self.receiver} : {self.content}"

    def get_last_message(sender, receiver):
        last_message = Message.objects.filter(sender=sender, receiver=receiver).first()
        return last_message

    def get_absolute_url(self):
        return f'/messaging/{self.user.id}/'




class ReserveMealMessage(Message):
    accept_reject = models.BooleanField(blank=True, null=True)
    anonymous = models.BooleanField(default=False)


    def __str__(self):
        self.sender = super().sender
        self.content = super().content
        return f"From {self.sender} to {self.receiver} : {self.content}"

    def get_absolute_url(self):
        return f'/messaging/{self.user.id}/'

class BookstoreMessage(Message):
    pass
