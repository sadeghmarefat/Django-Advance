from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, ListView
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


class PostList(ListView):
    # model = Post
    queryset = Post.objects.all()
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        qs = super().get_queryset()
        return  qs.filter(status=True).order_by('-created_at')


