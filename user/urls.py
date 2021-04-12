from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic import TemplateView


from user import views
from forum import views as fviews

app_name = 'user'



urlpatterns = [
    path('login/', views.userlogin, name='user_login'),
    path('userid=<int:user_ID>/', views.userDetail, name='userDetail'),
    path('regis/', views.userregister, name='registration'),
    path('user_ok/', views.user_ok, name='user_ok'),
    path('logout/', views.userlogout, name='user_logout'),
    path('findpw/',views.findPassword,name='findpassword'),
    path('post_update/<int:pk>/',
        login_required(fviews.PostUpdate.as_view()),
        name='post_update'),
    path('post_delete/<int:pk>/',
        login_required(fviews.PostDelete.as_view()),
        name='post_delete'),

    # path('')
    #path('contest/<int:contest_id>/', views.detail,name='detail'),

    #path('vote/<int:user_ID>/', views.vote, name='vote'),

    #path('test/', views.IndexView(),name='test'),

]