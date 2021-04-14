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
    path('friendsadd/<int:friend_id>', views.makefriends, name='makefriends'),
    path('friendsdelete/<int:friend_id>', views.deletefriends, name='deletefriends'),
    path('applylist/', views.applyList, name='applyList'),

    # when follow a contest
    path('followCon/contest_id=<int:contest_id>', views.followContest, name='followCon'),
    path('cancelFol/contest_id=<int:contest_id>', views.cancelFollowContest, name='cancelFol'),
    # when select one contest and look for team
    path('teamlist/contest_id=<int:contest_id>', views.teamList, name='teamList'),
    path('teampage/team_id=<int:team_id>', views.teamDetail, name='teamDetail'),
    path('addteam/team_id=<int:team_id>&contest_id=<int:contest_id>', views.addTeam, name='addTeam'),
    path('sendapp/team_id=<int:team_id>&contest_id=<int:contest_id>&user_id=<int:user_id>', views.sendapp, name='sendApp'),
    #path('teamcreate/contest_id=<int:contest_id>', views.TeamCreate, name='teamCreate'),

    #path('vote/<int:user_ID>/', views.vote, name='vote'),
    #path('test/', views.IndexView(),name='test'),
]