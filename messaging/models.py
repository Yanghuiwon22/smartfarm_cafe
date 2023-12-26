from django.db import models
from django.contrib.auth.models import User
from itertools import chain

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = f'{sender}_{receiver}'

    def __str__(self):
        return f"From {self.sender} to {self.receiver} : {self.content}"

    def get_last_message(sender, receiver):
        last_message = Message.objects.filter(sender=sender, receiver=receiver).first()
        return last_message

    def get_absolute_url(self):
        return f'/messaging/{self.user.id}/'

    def get_room(self):
        return
