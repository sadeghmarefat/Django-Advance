from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .forms import ContactForm, CreateForm
from .models import Post
# Create your views here.

# function based views
# def indexView(request):
#     name = 'Sadegh'
#     context = {'name': name}
#     return render(request, 'index.html', context)
#

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Sadegh'
        context['posts'] = Post.objects.all()
        return context


class RedirectToIndex(RedirectView):
    pattern_name='blog:cbv_index'


class PostListView(LoginRequiredMixin,ListView):
    model = Post
    # queryset = Post.objects.all()
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        qs = super().get_queryset()
        return  qs.filter(status=True).order_by('-created_at')


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/blog/posts"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)


class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = CreateForm
    success_url = '/blog/posts/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = CreateForm
    success_url = '/blog/posts'


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = '/blog/posts'