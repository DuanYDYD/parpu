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
from user.form import UserForm, ForgetForm, TeamForm, ApplicationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from user.models import User, Friend, Team, Application
from forum.models import  Column, Comment, Friend, Post
from contest.models import Contest
from django.shortcuts import get_object_or_404, render
import logging

from user.utils import random_str

logger = logging.getLogger(__name__)

PAGE_NUM = 50

# Create your views here.




def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #user.levels += 1  #登录一次积分加 1
            #user.save()
        return redirect('user:userDetail')
    else:
        return render(request, 'login.html', None)

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
                return render(request, 'user_fail.html', {"errors": errors})
        return redirect('user:userDetail')
    else:
        form = UserForm()
        # next = request.GET.get('next',None)
        # if next is None:
        # next = reverse_lazy('index')
        return render(request, 'register.html', {"form": form})


code = ''
def findPassword(request):
    errors = []
    global code
    if request.method == 'POST':
        email = request.POST.get("email", "")
        form = ForgetForm(request.POST)
        if form.is_valid():
            code = random_str(16)
            title = 'Please enter the verification code to find your password.'
            message = "Here is your verification code ！\n\n" + code
            from_email = None
            try:
                send_mail(title, message, from_email, [email])
            except Exception as e:
                logger.error(
                    '[UserControl]Cannot reach the registration email:[%s]' % email)
                return HttpResponse("Error in sending email.\nPassword finding fails!", status=500)
        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())
            if errors:
                return render(request, 'user/user_fail.html', {"errors": errors})
        ##########################
        backcode=request.POST.get("backcode", "")

        if backcode == code:
            thisuser = get_object_or_404(User,email=email)
            password = thisuser.password
            title = 'Successfully find your password.'
            message = str(password)
            from_email = None
            try:
                send_mail(title, message, from_email, [email])
            except Exception as e:
                logger.error(
                    '[UserControl]Cannot reach the registration email:[%s]' % email)
                return HttpResponse("Error in sending email.\nPassword finding fails!", status=500)
        return redirect('index')
    else:
        form = ForgetForm()
        return render(request, 'user/form.html', {"form": form})

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
def addInteresetedContest(request, contest_id):
    user = User.objects.get(pk=request.user.id)
    try:
        contest = user.interestedContest.get(pk=contest_id)
    except:
        contest = None
    if contest:
        user.interestedContest.add(contest)
        user.save()
        return HttpResponse('<script>alert("Successfully added it！");window.history.back(-1);"</script>')
    else:
        return HttpResponse('<script>alert("you have added it！");window.history.back(-1);"</script>')

@login_required
def makefriends(request, friend_id):
    p = get_object_or_404(User,pk=friend_id)
    try:
        Friend.objects.get(user=request.user, to=p)
        return HttpResponse("You have added the friend")
    except:
        newFriend = Friend.objects.create(user=request.user, to=p)
        newFriend.save()
        return HttpResponse("Added!")


@login_required
def deletefriends(request, friend_id):
    p = get_object_or_404(User, pk=friend_id)
    try:
        friend= Friend.objects.get(user=request.user,to=p)
        friend.delete()
        return HttpResponse("You delete the friend！<a href='/'>return</a>")
    except:
        return HttpResponse("You don't have the friend！<a href='/'>return</a>")

@login_required
def followContest(request, contest_id): #这个urls要做到contest那里
    thiscontest = get_object_or_404(Contest, pk=contest_id)
    user = get_object_or_404(User, pk=request.user.id)
    if user.objects.filter(interestedContest=thiscontest).exists():
        return HttpResponse('<script>alert("you have added it！");window.history.back(-1);"</script>')
    else:
        user.interestedContest.add(thiscontest)
        user.save()
        return HttpResponse('<script>alert("Successfully add it！");window.history.back(-1);"</script>')

@login_required
def cancelFollowContest(request, contest_id):
    thiscontest = get_object_or_404(Contest, pk=contest_id)
    user = get_object_or_404(User, pk=request.user.id)
    if user.objects.filter(interestedContest=thiscontest).exists():
        user.interestedContest.remove(thiscontest)
        user.save()
        return HttpResponse('<script>alert("Successfully cancel it!");window.history.back(-1);"</script>')
    else:
        return HttpResponse('<script>alert("you have not added it！");window.history.back(-1);"</script>')

@login_required()
def TeamCreate(request,contest_id):
    thiscontest = get_object_or_404(Contest, pk=contest_id)
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        form = TeamForm()
        name = request.POST.get("name", "")
        capacity = request.POST.get("capacity", "")
        announce = request.POST.get("announce", "")
        requirement = request.POST.get("requirement", "")

        form = TeamForm(request.POST)
        errors = []
        if form.is_valid():
            team = Team()
            team.contest = thiscontest
            team.leader = user
            team.name = name
            team.capacity = int(capacity)
            team.requirement = requirement
            team.announce = announce
            team.save()
            return HttpResponse('<script>alert("Successfully create it!");window.history.back(-1);"</script>')
        else:
            for k, v in form.errors.items():
                #v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())
            if errors:
                return render(request, 'user/user_fail.html', {"errors": errors})
    else:
        form = TeamForm()
        return render(request, 'user/form.html', {"form": form})

def teamDetail(request, team_id):
    thisTeam = get_object_or_404(User, pk=team_id)
    context = {
        'team': thisTeam,
    }
    return render(request, 'user/teampage.html', context)

def teamList(request, contest_id):
    try:
        Contest.objects.get(pk=contest_id)
        thiscontest = Contest.objects.get(pk=contest_id)
        team_list = Team.objects.filter(contest=thiscontest)
        return render(request, 'user/list.html', {'team_list' : team_list} )
    except:
        return HttpResponse('<script>alert("We do not have the contest");window.history.back(-1);"</script>')


@login_required
def addTeam(request, team_id): #有一个bug，没法检测同一个contest里这个人加了很多队伍
    if request.method == 'GET':
        team = Team.objects.filter(pk=team_id).first()
        user = User.objects.get(pk=request.user.id)
        if team.capacity <= team.team_members.all().count()+1:
            return HttpResponse('full')
            #return HttpResponse('<script>alert("The team is full!");window.history.back(-2);"</script>')
        else:
            application = Application.objects.filter(sender=request.user, team=get_object_or_404(Team, pk=team_id))
            if len(application) != 0:
                return HttpResponse('sented')
                #return HttpResponse('<script>alert("You have sent the application!");window.history.back(-2);"</script>')
            else:
                form = ApplicationForm()
                return render(request, 'user/form.html', {"form": form})

@login_required()
def applyList(request):
    user = User.objects.get(pk=request.user.id)
    try:
        team = Team.objects.get(leader=user)
    except:
        team = None
    application_list = Application.objects.filter(team=team)
    return render(request,'user/list.html',{'application_list':application_list})

@login_required
def applydetail(request,application_id):
    if request.method == 'GET':
        application = get_object_or_404(Application, pk=application_id)
        return render(request, 'user/list.html', {'application': application})
    else:
        application = get_object_or_404(Application, pk=application_id)
        flag = request.POST.get('flag', '')
        user = User.objects.get(pk=request.user.id)
        sender = Application.sender
        team = Team.objects.get(leader=user)
        team.team_members.add()
        team.save()

        if team.capacity <= team.team_members.all().count()+1:
            application.delete()
            return HttpResponse('<script>alert("The team is full!");window.history.back(-2);"</script>')

        elif flag == 'yes':
            application.delete()
            team.team_members.add(sender)
            team.save()
            return HttpResponse('<script>alert("Successfully add in!");window.history.back(-2);"</script>')

        else:
            application.delete()
            return HttpResponse('<script>alert("Successfully dismiss it!");window.history.back(-2);"</script>')

