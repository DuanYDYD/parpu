from django.urls import path
from django.views.generic import TemplateView


from forum import views

app_name = 'forum'
urlpatterns = [

    path('',views.forumindex,name='index'),
    path('column=<int:column_id>/',
        views.columnIndex,
        name='columnIndex'),
    path('post_create/',
        views.PostCreate,
        name='post_create'),
    path('column=<int:column_id>/post=<post_id>/',
        views.postDetail,
        name='post_detail'),
    # path('column=<int:column_id>/post=<post_id>/commentCreate/',
    #     views.commentCreate,
    #     name='comment_create'),
    path('column=<int:column_id>/post=<post_id>/likePost/',views.likePost,name='likePost'),
    path('test/',views.test,name='test')
    # path
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