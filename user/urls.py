from django.urls import path
from django.views.generic import TemplateView


from user import views

app_name = 'user'
urlpatterns = [
    path('login/', views.userlogin, name='user_login'),
    path('userid=<int:user_ID>/', views.userDetail, name='userDetail'),
    path('regis', views.userregister, name='registration'),
    path('user_ok', views.user_ok, name='user_ok'),
    path('logout/', views.userlogout, name='user_logout'),
    #path('contest/<int:contest_id>/', views.detail,name='detail'),

    #path('vote/<int:user_ID>/', views.vote, name='vote'),

    #path('test/', views.IndexView(),name='test'),
]