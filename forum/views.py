import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# Create your views here.
from user.form import UserForm
from forum.form import PostForm  # ,MessageForm, PostForm,
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from forum.models import Contest, Column, Comment, Post
from user.models import User, Friend, Team
from django.shortcuts import get_object_or_404, render
import logging

logger = logging.getLogger(__name__)

PAGE_NUM = 50


# class BaseMixin(object):
#     def get_context_data(self, *args, **kwargs):
#         context = super(BaseMixin, self).get_context_data(**kwargs)
#         try:
#             context['nav_list'] = Nav.objects.all()
#             context['column_list'] = Column.objects.all()[0:5]
#             context['last_comments'] = Comment.objects.all().order_by(
#                 "-created_at")[0:10]
#             # if self.request.user.is_authenticated():
#             #     k = Notice.objects.filter(
#             #         receiver=self.request.user, status=False).count()
#             #     context['message_number'] = k
#
#         except Exception as e:
#             logger.error(u'[BaseMixin]Loggin wrong')
#
#         return context


#首页
# class IndexView(BaseMixin, ListView):
#     model = Post
#     queryset = Post.objects.all()
#     template_name = 'index.html'
#     context_object_name = 'post_list'
#     paginate_by = PAGE_NUM  #分页--每页的数目
#
#     def get_context_data(self, **kwargs):
#         kwargs['foruminfo'] = get_forum_info()
#         kwargs['online_ips_count'] = get_online_ips_count()
#         kwargs['hot_posts'] = self.queryset.order_by("-responce_times")[0:10]
#         return super(IndexView, self).get_context_data(**kwargs)



# class UserdetailView(BaseMixin, ListView):
#     """通用视图"""
#     model = User     #指定类
#     context_object_name = 'Users'    #contests被传到模板中
#     template_name = "user_list.html"  #渲染页面


def columnIndex(request, column_id):
    """Listing of posts in a topic."""
    column = get_object_or_404(Column, pk=column_id)
    posts = Post.objects.filter(column=column).order_by("created_at")
    # try:
    #     user = request.user.id
    # except:
    #     user = None
    # topic = Topic.objects.get(pk=topic_id)
    # topic.sum_visits(user)
    context = {
        'column' : column,
        'posts' : posts,
    }
    return render(request, "forum/columnDetail.html",context)


@login_required
def PostCreate(request, column_id):
    column = Column.objects.get(id=column_id)
    author = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        form = PostForm(request.POST)
        errors = []
        if form.is_valid():

            post = Post()
            post.title = title
            logger.error(form['title'])
            post.content = content
            post.author = author
            post.column = column
            post.save()
            request.POST.get_absolute_url()
            return HttpResponse("发贴成功！<a href= '' >返回</a>")
        else:
            #如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                #v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())
            if errors:
                return render(request, 'user/user_fail.html', {"errors": errors})
    else:
        form = PostForm()
        #next = request.GET.get('next',None)
        #if next is None:
        #next = reverse_lazy('index')
        return render(request, 'user/form.html', {"form" : form})

#编辑贴
class PostUpdate(UpdateView):
    model = Post
    template_name = 'user/form.html'
    success_url = reverse_lazy('forum:index')


#删贴
class PostDelete(DeleteView):
    model = Post
    template_name = 'forum/delete_confirm.html'
    success_url = reverse_lazy('forum:index')

# def Comment(request, slug, topic_id):
#
#     quote = request.GET.get('quote', '')
#     author = request.GET.get('author', '')
#     if quote:
#         quote = '<blockquote>' + quote + '<footer>' + author + '</footer></blockquote>'
#
#     forum = get_object_or_404(Forum, slug=slug)
#     posts = Post.objects.filter(topic=topic_id).order_by("created").reverse()[:3]
#     topic = Topic.objects.get(pk=topic_id)
#
#     form_title = ''
#     if topic.last_post():
#         form_title = 'Re: ' + topic.last_post().title.replace('Re: ', '')
#
#     default_data = {'title': form_title}
#     form = PostForm(initial=default_data)
#
#     if request.method == 'POST':
#         quote = request.POST.get('quote', '')
#         form = PostForm(request.POST)
#
#         if form.is_valid():
#
#             post = Post()
#             post.topic = topic
#             post.title = form.cleaned_data['title']
#             post.body = quote + form.cleaned_data['body']
#             post.creator = request.user
#             post.user_ip = request.META['REMOTE_ADDR']
#
#             post.save()
#             return HttpResponseRedirect(reverse_lazy('topic-detail', args=(slug, topic.id, )))
#
#     return render(request, 'django_forum_app/reply.html', {'form': form, 'topic': topic, 'forum': forum, 'posts': posts, 'quote': quote})