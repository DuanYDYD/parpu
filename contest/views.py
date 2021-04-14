from django.shortcuts import get_object_or_404, render
from contest.models import Contest
from django.db.models import Max, Min
from forum.models import Post, Column
from django.db import models

def index(request):
    context = {}
    recent_contest = Contest.objects.order_by("-id")[0:6]
    con_number = Contest.objects.all().aggregate(Max('id'))
    recent_post = Post.objects.order_by("-id")[0:3]
    return render(request, "ContestSearch.html", {"recent": recent_contest, "contest_number": con_number['id__max'],
                                                  "post": recent_post})

def contestpage(request):
    contest_id = request.GET.get('contest_id')
    requested = get_object_or_404(Contest, pk=contest_id)
    deadline = requested.regi_ddl.strftime('%Y-%m-%d')
    deadline = deadline.replace('-', '/')
    return render(request, "ContestPage.html", {"contest": requested, "deadline": deadline})

def addpost(request):
    return render(request, "AddPost.html")

# Create your views here.
