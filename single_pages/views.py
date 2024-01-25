from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
# from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login






# Create your views here.
def landing(request):
    return render(
        request,
        'single_pages/landing.html'
                  )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
                  )

def smartfarm_landing(request):
    return render(request, 'single_pages/landing.html')

def my_page(request):
    return render(
        request,
        'single_pages/my_page.html'
                  )

def custom_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)


        if user is not None and check_password(password, user.password):
            login(request, user)

            # 로그인 성공 시 리다이렉션할 페이지 지정
            return redirect('smartfarm_landing')

        else:
            # 로그인 실패 처리
            messages.error(request, "사용자를 찾을 수 없거나 입력하신 비밀번호가 정확하지 않습니다.다시 시도해 주세요.")
            return render(request, 'single_pages/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'single_pages/login.html')

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)
            return redirect('smartfarm_landing')


    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'single_pages/sign_up.html', context)



def custom_logout(request):
    logout(request)
    return redirect('smartfarm_landing')