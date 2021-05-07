from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Article, Comment, Like
from django.core.paginator import Paginator
from blog.forms import CommentForm, ArticleForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.contrib import messages
from common import common
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        print(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            common.send_line_notify(f'{request.user}さんが新しい記事を投稿しました。\n「{article.title}」\n{request.build_absolute_uri()}')
    objs = Article.objects.order_by('-updated_at')
    paginator = Paginator(objs, 5)
    page_number = request.GET.get('page')
    context = {
        'page_obj':paginator.get_page(page_number),
        'page_number':page_number,    
    }
    return render(request, 'blog/blogs.html', context)

def article(request, pk):
    obj = get_object_or_404(Article, pk=pk)
    print(obj)
    if request.method == 'POST':
        if 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)        
                comment.user = request.user
                comment.article = obj
                comment.save()
        elif 'edit' in request.POST:
            form = ArticleForm(request.POST)
            if form.is_valid():
                edit_article = form.save(commit=False)        
                obj.title = edit_article.title
                obj.text = edit_article.text
                obj.save()
                messages.success(request, '編集が完了しました')
        elif 'delete' in request.POST:
            obj.delete()
            messages.success(request, '削除が完了しました')
            return redirect('articles')
    comments = Comment.objects.filter(article=pk)
    like_count = Like.objects.filter(article=pk).count()
    context = {'article':obj, 'comments':comments, 'like_count':like_count}
    print(obj.author,request.user)
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
