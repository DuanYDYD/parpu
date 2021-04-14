from django.shortcuts import get_object_or_404, render
from contest.models import Contest
from django.db.models import Max, Min, Count
from forum.models import Post, Column
from django.db import models

def index(request):
    recent_contest = Contest.objects.order_by("-id")[0:6]
    con_number = Contest.objects.all().aggregate(Max('id'))
    recent_post = Post.objects.order_by("-id")[0:3]
    return render(request, "ContestSearch.html", {"recent": recent_contest, "contest_number": con_number['id__max'],
                                                  "post": recent_post})

def search(request):
    if request.method == 'GET':
        area = request.GET.get('area')
        area = area.lower()
        requested = Contest.objects.filter(area=area).all()
        if requested.count() > 0:
            return render(request, "contestrequested.html", {"contest": requested})
        else:
            return render(request, "contestrequested.html", {"msg": "Sorry, no contest meets the requirement"})
    elif request.method == 'POST':
        cname = request.POST.get('con_name')
        requested = Contest.objects.filter(name=cname).all()
        if requested.count() > 0:
            return render(request, "contestrequested.html", {"contest": requested})
        else:
            return render(request, "contestrequested.html", {"msg": "Sorry, no contest meets the requirement"})

def contestpage(request):
    contest_id = request.GET.get('contest_id')
    requested = get_object_or_404(Contest, pk=contest_id)
    deadline = requested.regi_ddl.strftime('%Y-%m-%d')
    deadline = deadline.replace('-', '/')
    return render(request, "ContestPage.html", {"contest": requested, "deadline": deadline})

def addpost(request):
    return render(request, "AddPost.html")

# Create your views here.
