from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from bookstore.models import BookStore, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from messaging.views import MessageForm
import pandas as pd
import requests



class BookStoreList(ListView):
    model = BookStore
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(BookStoreList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = BookStore.objects.filter(category=None).count()
        return context

class BookStoreDetail(DetailView):
    model = BookStore
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super(BookStoreDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = BookStore.objects.filter(category=None).count()
        return context

class BookForm_Form(LoginRequiredMixin, CreateView):
    model = BookStore
    fields = ['isbn', 'title', 'author', 'publisher', 'price_set', 'price', 'img_file', 'content', 'traces', 'status']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.writer = current_user

            kwd = requests.GET.get("kwd")
            if kwd:
                form.cleaned_data['title'] = get_book_info(kwd).get('title', '')
                form.cleaned_data['author'] = get_book_info(kwd).get('author', '')

            return super(BookForm_Form, self).form_valid(form)

        else:

            return redirect('/bookstore/bookstore_list')

def get_book_info(request, kwd):
    url = "https://www.nl.go.kr/NL/search/openApi/search.do"


    # ---- ex. 메일에 있는 데이터가 표시되는 다른 장치의 모델 데이터
    params = {
        "key": "09923c9111df84fef5b709ca39b2489a275bf60603e848b4cc21ac4597aabfd6",
        "kwd": kwd,
        "apiType": 'json'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:  # 성공적인 응답
        content_type = response.headers.get('Content-Type')
        if 'charset=' in content_type:
            encoding = content_type.split('charset=')[-1]
            data = json.loads(response.content.decode(encoding))
        else:
            data = json.loads(response.content.decode("UTF-8"))

    else:
        data = '오류'

    return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, status=200)


def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    book_list = BookStore.objects.filter(category=category)

    return render(
        request,
        'bookstore/bookstore_list.html',
        {
            'book_list' : book_list,
            'categories' : Category.objects.all(),
            'no_category_post_count':BookStore.objects.filter(category=None).count(),
            'category':category,
        }
    )

def send_bookstore_message(request, pk):
    book = BookStore.objects.filter(pk=pk).first()
    if request.method == 'POST':
        form = MessageForm(request.POST, hide_receiver=True)
        # form = BookForm_Form(request.POST, hide_receiver=True)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.receiver = book.writer
            new_message.save()
            return redirect('message_list')  # 쪽지가 성공적으로 전송되었음을 나타내는 페이지로 리다이렉트
    else:
        form = MessageForm(request.POST, hide_receiver=True)

    return render(request, 'messaging/message_form.html', {'form': form})

def bookstore_sold(request, pk):
    book = get_object_or_404(BookStore, pk=pk)
    book.is_sold = True  # 판매 완료 상태를 표시하는 필드를 업데이트합니다.

    if book.is_sold:
        book.delete()
    return render(request, 'bookstore/bookstore_soldout.html')






