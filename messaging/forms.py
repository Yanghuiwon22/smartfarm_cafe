from django import forms
from .models import Message, ReserveMealMessage


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        hide_receiver = kwargs.pop('hide_receiver', False)
        super(MessageForm, self).__init__(*args, **kwargs)

        if hide_receiver:
            self.fields['receiver'].widget = forms.HiddenInput()  # receiver 필드를 숨깁니다.
            self.fields['receiver'].required = False

    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class ReserveMealMessageForm(forms.ModelForm):
    class Meta:
        model = ReserveMealMessage

        # fields 안에 들어가는 값은 자동으로 처리되는 부분이 아닌 사용자가 직접 처리해야 하는 부분
        fields = ['content', 'anonymous', 'accept_reject']