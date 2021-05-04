from django.shortcuts import render, redirect
from blog.models import Article
from django.contrib.auth.views import LoginView
from mysite.forms import UserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.mail import send_mail

# Create your views here.

def index(request):
    ranks = Article.objects.raw("""
        select *
        from blog_article
        where id in 
        (select blog_article.id
        from blog_article
        inner join blog_like
        on blog_article.id = blog_like.article_id
        group by blog_article.id
        order by count(blog_article.id)
        limit 2)
    """)
    objs = Article.objects.all()[:3]
    context = {'articles':objs, 'ranks':ranks}
    return render(request, 'mysite/index.html', context)

class Login(LoginView):
    template_name = 'mysite/auth.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログイン完了')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'ログインエラー')
        return super().form_invalid(form)

def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print("post")
        if form.is_valid():
            print("valid")
            user = form.save(commit=False)
            user.save()

            login(request, user)
            
            messages.success(request, '登録完了')
            return redirect('/')
    return render(request, 'mysite/auth.html', context)

@login_required
def mypage(request):
    context = {}
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, '更新完了')
    return render(request, 'mysite/mypage.html', context)

def contact(request):
    context = {}
    if request.method == 'POST':
        subject = 'お問い合わせがありました'
        message = request.POST.get('content')
        email_from = 'shigi19971204@gmail.com'
        email_to = ['shigi19971204@gmail.com']
        send_mail(subject, message, email_from, email_to)
        messages.success(request,'お問い合わせありがとうございます。')
    return render(request, 'mysite/contact.html', context)