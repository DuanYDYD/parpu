import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# Create your views here.
from user.form import UserForm, ForgetForm, TeamForm
from forum.form import PostForm, CommentForm  # ,MessageForm, PostForm,
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from forum.models import  Column, Comment, Post, PostLike, CommentLike
from user.models import User, Friend, Team
from contest.models import Contest
from django.shortcuts import get_object_or_404, render
import logging

logger = logging.getLogger(__name__)

PAGE_NUM = 50



def columnIndex(request, column_id):
    """Listing of posts in a topic."""
    column = get_object_or_404(Column, pk=column_id)
    posts_list = Post.objects.filter(column=column).order_by("created_at")
    # try:
    #     user = request.user.id
    # except:
    #     user = None
    # topic = Topic.objects.get(pk=topic_id)
    # topic.sum_visits(user)
    context = {
        'column' : column,
        'posts_list' : posts_list,
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
            post.content = content
            post.author = author
            post.column = column
            post.save()
            #request.POST.get_absolute_url()
            return HttpResponseRedirect(reverse_lazy('forum:columnIndex',kwargs={'column_id': column_id}))
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
    form_class = PostForm
    template_name = 'user/form.html'
    success_url = reverse_lazy('index')

#删贴
class PostDelete(DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'forum/delete_confirm.html'
    success_url = reverse_lazy('index')

def postDetail(request, column_id, post_id):
    column = get_object_or_404(Column, pk=column_id)
    post = get_object_or_404(Post, pk=post_id)
    comments_list = Comment.objects.filter(post=post)
    context = {
        'column': column,
        'post': post,
        'comments_list': comments_list,
    }
    return render(request, "forum/postDetail.html", context)

@login_required
def commentCreate(request, column_id, post_id):
    post = Post.objects.get(id=post_id)
    author = User.objects.get(pk=request.user.id)
    errors = []
    if request.method == 'POST':
        content = request.POST.get("content", "")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.post = post
            comment.author = author
            comment.content = content
            comment.save()
            return HttpResponseRedirect(reverse_lazy('forum:post_detail', kwargs={'column_id': column_id,
                                                                                  'post_id':post_id}))
        else:
        # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
            # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())
            if errors:
                return render(request, 'user/user_fail.html', {"errors": errors})

    else:
        form = CommentForm()
        return render(request, 'user/form.html', {"form" : form})

@login_required
def likePost(request, post_id): #还没做url
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if PostLike.objects.filter(liker=user, post=post).exists():
        return HttpResponse('<script>alert("you have already liked！");window.history.back(-1);"</script>')
    else:
        post.like_num += 1
        post.save()
    return HttpResponse('<script>alert("you like it！");window.history.back(-1);"</script>')

@login_required #如何传入comment_id 还需商讨 还没做url
def likeComment(request, comment_id):
    comment = get_object_or_404(Post, pk=comment_id)
    user = request.user
    if CommentLike.objects.filter(liker=user, post=comment).exists():
        return HttpResponse('<script>alert("you have already liked！");window.history.back(-1);"</script>')
    else:
        comment.like_num += 1
        comment.save()
    return redirect('forum:post_detail')