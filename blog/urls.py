from django.urls import path
from blog import views


urlpatterns = [
    path('', views.index, name='articles'),
    path('<int:pk>/', views.article, name='article'),
    path('<int:pk>/like', views.like, name='like'),
]