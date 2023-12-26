from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Archive
from django.contrib.auth.mixins import LoginRequiredMixin

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
        fields = ['title', 'author', 'professor', 'subject', 'student', 'content', 'file_upload', 'head_image']

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

