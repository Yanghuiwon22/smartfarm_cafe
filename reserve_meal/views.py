from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from messaging.models import ReserveMealMessage
from .models import ReserveMeal
from itertools import chain
from django.views.generic import CreateView,DetailView
from messaging.views import MessageForm

# Create your views here.
class ReserveMealDetail(DetailView):
    model = ReserveMeal
    context_object_name = 'meal'


def mypage_meal(request):
    sent_meals = ReserveMealMessage.objects.filter(sender=request.user).order_by('-timestamp')
    received_meals = ReserveMeal.objects.filter(receiver=request.user).order_by('-timestamp')

    all_meals = list(chain(sent_meals, received_meals))

    return render(request, 'reserve_meal/mypage_meal.html',
                  { 'all_meals':all_meals})
@login_required
def reserve_list(request):
    all_meals = ReserveMealMessage.objects.all().order_by('-timestamp')
    # all_meals = ReserveMeal

    return render(request, 'reserve_meal/reservemeal_list.html',
                  {'all_meals': all_meals})


def send_reserve_message(request, pk):
    meals = ReserveMeal.objects.filter(pk=pk).first()


    if request.method == 'POST':
        form = MessageForm(request.POST, hide_receiver=True)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.receiver = meals.sender
            new_message.anonymous = True
            new_message.save()
            return redirect('message_list')  # 쪽지가 성공적으로 전송되었음을 나타내는 페이지로 리다이렉트
    else:
        form = MessageForm(request.POST, hide_receiver=True)

    return render(request, 'reserve_meal/send_reserve_message.html',
                  {
                    'meals' : meals,
                    'form' : form
                  })

class ReserveMeal_Form(CreateView):
    model = ReserveMeal
    fields = ['receiver','timetable','content', 'anonymous']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.sender = current_user
            form.anonymous = False
            return super(ReserveMeal_Form, self).form_valid(form)

class ReserveMeal_Form_Secret(CreateView):
    model = ReserveMeal
    fields = ['food','content', 'anonymous','title']
    template_name = 'reserve_meal/reservemeal_form_secret.html'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.sender = current_user
            form.instance.anonymous = True
            return super(ReserveMeal_Form_Secret, self).form_valid(form)







