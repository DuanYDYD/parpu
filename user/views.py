from django.shortcuts import render
import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from forum.form import  PostForm # ,MessageForm, PostForm,
from user.form import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from user.models import User, Friend
from forum.models import Contest,  Column, Comment, Friend, Post
from django.shortcuts import get_object_or_404, render
import logging

logger = logging.getLogger(__name__)

PAGE_NUM = 50
# Create your views here.
def index(request):
    latest_contest_list = Contest.objects.all()

    context = {
        'latest_contest_list': latest_contest_list,

    }
    return render(request, 'user/index.html', context)




def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next = request.POST['next']


        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #user.levels += 1  #登录一次积分加 1
            #user.save()
        return HttpResponseRedirect(next)
    else:
        next = request.GET.get('next', None)
        if next is None:
            next = reverse_lazy('index')
        return render(request, 'user/login.html', {'next': next})

def userregister(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        email = request.POST.get("email", "")
        sex = request.POST.get("sex", "")
        major = request.POST.get("major", "")

        form = UserForm(request.POST)
        errors = []
        #验证表单是否正确
        if form.is_valid():
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            title = "Welcome to parpu"
            message = "Hi！ %s ,thanks for the registration %s ！\n\n" % (username,site_name) +\
                      "Please keep it in mind：\n" + \
                      "Username：%s" % username+"\n" + \
                      "Email for registration：%s" % email+"\n" + \
                      "Our site：http://%s" % domain+"\n\n"
            from_email = None
            try:
                send_mail(title, message, from_email, [email])
            except Exception as e:
                logger.error(
                    '[UserControl]Cannot reach the registration email:[%s]/[%s]' % (username, email))
                return HttpResponse("Error in sending email.\nRegistration fails!", status=500)

            new_user = form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
        else:
            #如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                #v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())
            if errors:
                return render(request, 'user/user_fail.html', {"errors": errors})
        return redirect('user:user_ok')

    else:
        form = UserForm()
        #next = request.GET.get('next',None)
        #if next is None:
        #next = reverse_lazy('index')
        return render(request, 'user/register.html', {"form" : form})

def user_ok(request):
    time.sleep(5)
    return redirect('index')

def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))

def IndexView(request):
    """通用视图"""
    context = {
        'column_list' : Column.objects.all()[0:5],
        'last_comments' : Comment.objects.all().order_by("-created_at")[0:10],
        'contest_list' : Contest.objects.all(),
        'hot_contests': Contest.objects.all().order_by("interested_num")[0:5],
    }

    paginate_by = PAGE_NUM  #分页--每页的数目  #渲染页面
    if request.user.is_authenticated:
        friendlist=Friend.objects.filter(user=request.user)
        context['friends_list'] = []
        if len(friendlist)!=0:
            userlist=[]
            for friend in friendlist:
                userlist.append(friend.to)
            context['friends_list'] = userlist

    return render(request, 'user/indexTest.html', context)

def userDetail(request, user_ID):
    thisUser = get_object_or_404(User, pk=user_ID)
    context = {
        'user' : thisUser,
    }
    return render(request, 'user/userpage.html', context)

@login_required
def makefriends(request, friend_id):
    if Friend.objects.filter(user=request.user,to=User.objects.get(friend_id)):
        return HttpResponse("You have added the friend")
    else:
        newFriend=Friend.objects.create(user=request.user,to=User.objects.get(friend_id))
        newFriend.save()
        return HttpResponse("Added!")

@login_required
def deletefriends(request, friend_id):
    if Friend.objects.filter(user=request.user,to=User.objects.get(friend_id)):
        obj = Friend.objects.get(id=friend_id)
        obj.delete()
        return HttpResponse("You delete the friend！<a href='/'>return</a>")
    else:
        return HttpResponse("You don't have the friend！<a href='/'>return</a>")