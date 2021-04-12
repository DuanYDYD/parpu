from django.urls import path
from django.views.generic import TemplateView


from forum import views

app_name = 'forum'
urlpatterns = [

    #path('contest/<int:contest_id>/', views.detail,name='detail'),

    #path('vote/<int:user_ID>/', views.vote, name='vote'),

    #path('test/', views.IndexView(),name='test'),
    path('column=<int:column_id>/post_create',
        views.PostCreate,
        name='post_create'),
    # path('user/post_update/(?P<pk>\d+)/$',
    #     login_required(PostUpdate.as_view()),
    #     name='post_update'),
    # url(r'^user/post_delete/(?P<pk>\d+)/$',
    #     delete_permission(login_required(PostDelete.as_view())),
    #     name='post_delete'),
    # url(r'^user/post_delete/(?P<pk>\d+)/$',
    #     delete_permission(login_required(PostDelete.as_view())),
    #     name='post_delete'),
]