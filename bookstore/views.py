from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import BookStore, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from messaging.views import MessageForm

from django.urls import reverse
from django.http import HttpResponseRedirect
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
    fields = ['title', 'author', 'publisher', 'price_set', 'price', 'img_file', 'content', 'traces', 'status']
    # success_url = reverse_lazy('bookstore_list')  # 'bookstore_list'는 실제로 리다이렉트할 URL 이름으로 수정해야 합니다.

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.writer = current_user
            return super(BookForm_Form, self).form_valid(form)
        else:
            return redirect('/bookstore/bookstore_list')

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

