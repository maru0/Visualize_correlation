from django.urls import path
from . import views

app_name = "cms"
urlpatterns = [
    # ここがユーザページ
    path('', views.IndexView.as_view(), name="indexview"),
    path('login/', views.LoginView.as_view(), name='regist'),
    path('logout/', views.LogoutView.as_view(), name='regist'),
    path('index/', views.IndexView.as_view(), name="index"),
    path('user/', views.index, name="user"),
    path('test/', views.IndexView.as_view(), name="indexview"),
    # path('', views.IndexView, name='index'),
    # path('views/',views.Userlist.index(),name='views'),
]
