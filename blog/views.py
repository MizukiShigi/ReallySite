from django.shortcuts import render
from blog.models import Article, Comment, Like
from django.core.paginator import Paginator
from blog.forms import CommentForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
# Create your views here.

def index(request):
    objs = Article.objects.all()
    paginator = Paginator(objs, 2)
    page_number = request.GET.get('page')
    context = {
        'page_obj':paginator.get_page(page_number),
        'page_number':page_number,    
    }
    return render(request, 'blog/blogs.html', context)

def article(request, pk):
    obj = Article.objects.get(pk=pk)
    print(obj)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)        
            comment.user = request.user
            comment.article = obj
            comment.save() 
    comments = Comment.objects.filter(article=pk)
    like_count = Like.objects.filter(article=pk).count()
    context = {'article':obj, 'comments':comments, 'like_count':like_count}
    return render(request, 'blog/article.html', context)

@ensure_csrf_cookie
def like(request, pk):
    obj = Article.objects.get(pk=pk)
    if request.method == 'POST':
        like_obj = Like.objects.filter(user=request.user, article=obj)
        if like_obj.exists():
            like_obj.delete()
            message = {'message':'minus_success'}
            return JsonResponse(message)
        else:
            like = Like.objects.create(user=request.user, article=obj)
            like.save()
            message = {'message':'add_success'}
            return JsonResponse(message)
