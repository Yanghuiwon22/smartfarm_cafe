from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Archive
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

class ArchiveList(ListView):
    model = Archive
    ordering = '-pk'

    # def get_context_data(self, **kwargs):
    #     context = super(ArchiveList, self).get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     context['no_category_post_count'] = Archive.objects.filter(category=None).count()
    #     return context

class ArchiveDetail(DetailView):
    model = Archive
    context_object_name = 'archive'

    # def get_context_data(self, **kwargs):
    #     context = super(ArchiveDetail, self).get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     context['no_category_post_count'] = Archive.objects.filter(category=None).count()
    #     return context

class ArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ['title', 'professor', 'subject', 'student', 'content', 'file_upload', 'head_image']

class ArchiveForm_Form(LoginRequiredMixin, CreateView):
    model = Archive
    form_class = ArchiveForm
    template_name = 'archive/archive_form.html'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.writer = current_user
            return super(ArchiveForm_Form, self).form_valid(form)
        else:
            return redirect('/archive/archive_list')
    # def get_success_url(self):
    #     return reverse('archive:archive_list')

def archiveform_view(request):
    if request.method == 'POST':
        form = ArchiveForm_Form(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.save()
            return redirect('archive:message_list')  # 'message_list'를 사용하려면 해당 URL을 정의해야 합니다.
    else:
        form = ArchiveForm()
    return render(request,'archive/archive_form.html', {'form': form})


def category_page(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        archive_list = Archive.objects.filter(category=category)

        return render(
            request,
            'archive/templates/archive/archive_list.html',
            {
                'archive_list': archive_list,
                'categories': Category.objects.all(),
                'no_category_post_count': Archive.objects.filter(category=None).count(),
                'category': category,
            }
        )
    except Category.DoesNotExist:
        # 처리하고자 하는 예외 발생 시 redirect 또는 다른 처리 추가
        return redirect('archive:archive_list')

class PostSearch(ArchiveList):
    # PostSearch에서는 검색된 결과를 한 페이지에 모두 보여주기 위해 PostList에 지정된 Pagination 속성을 해제한다.
    paginate_by = None

    def get_queryset(self):
        # URL을 통해 넘어온 검색어를 받아 q에 저장한다.
        q = self.kwargs['q']
        # title__contains처럼 title.contains 대신 밑줄 2개를 대신 사용하는 것에 유의한다.
        # 제목과 태그 모두에 '파이썬'이 포함된 경우 중복을 막기 위해 distinct를 사용한다.
        post_list = Archive.objects.filter(
            Q(title__contains=q) | Q(subject__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context