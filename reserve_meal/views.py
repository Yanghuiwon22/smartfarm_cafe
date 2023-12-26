from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ReserveMeal
from itertools import chain
from django.views.generic import CreateView,DetailView
from django.urls import reverse_lazy

# Create your views here.
class ReserveMealDetail(DetailView):
    model = ReserveMeal
    context_object_name = 'meal'

def reserve_main(request):
    all_users = User.objects.exclude(pk=request.user.pk)

    sent_meals = ReserveMeal.objects.filter(sender=request.user).order_by('-timestamp')
    received_meals = ReserveMeal.objects.filter(receiver=request.user).order_by('-timestamp')

    all_meals = list(chain(sent_meals, received_meals))

    return render(request, 'reserve_meal/reserve_main.html',
                  {'all_users': all_users, 'all_meals':all_meals})

def reserve_list(request):
    sent_meals = ReserveMeal.objects.filter(sender=request.user).order_by('-timestamp')
    received_meals = ReserveMeal.objects.filter(receiver=request.user).order_by('-timestamp')

    all_meals = list(chain(sent_meals, received_meals))

    return render(request, 'reserve_meal/reserve_list.html',
                  { 'all_meals':all_meals})

class ReserveMeal_Form(CreateView):
    model = ReserveMeal
    fields = ['receiver','timetable','content']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.sender = current_user
            return super(ReserveMeal_Form, self).form_valid(form)

class ReserveMeal_Form_Secret(CreateView):
    model = ReserveMeal
    fields = ['timetable','food','content']
    template_name = 'reserve_meal/reservemeal_form_secret.html'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.sender = current_user
            return super(ReserveMeal_Form, self).form_valid(form)




