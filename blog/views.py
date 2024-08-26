from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from .models import Post, Category
from .forms import PostForm, EditForm, DeleteForm
from django.urls import reverse_lazy,reverse

# Create your views here.


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    # ordering = ['-id' ]
    ordering = ['-date_created' ]
    paginate_by = 6


    def get_context_data(self, * args ,**kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(* args ,**kwargs)
        context["cat_menu"] = cat_menu
        
    #total likes
        for post in context['object_list']:
            post.total_likes = post.total_likes()
        return context

# like
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id')) # like
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user) # like
        liked - True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)])) # like



# function based view
def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request, 'blog/categories.html', {'cats': cats.title(), 'category_posts': category_posts })


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'blog/article_details.html'

    def get_context_data(self, * args ,**kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(* args ,**kwargs) #likes
        likes = get_object_or_404(Post, id=self.kwargs['pk']) #likes
        total_likes = likes.total_likes()

        liked = False
        if likes.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes #likes
        context['liked'] = liked
        return context


class AddCategoryView(CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'
    # fields = ('title', 'body')

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    # fields = '__all__'
    # fields = ('title', 'body')


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    form_class = EditForm
    # fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('home')
  


def about(request):
    return render(request, 'blog/about.html')

def faqs(request):
    return render(request, 'blog/faqs.html')
