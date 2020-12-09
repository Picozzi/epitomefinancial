from .models import Article
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    ordering = ['-date_posted']
    paginate_by = 4

class ArticleDetailView(DetailView):
    model = Article

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'main_story', 'mentioned_stock']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'main_story', 'mentioned_stock']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/bulletin/'
    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False