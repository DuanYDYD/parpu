from django.shortcuts import render
from contest.models import Contest

def index(request):
    requested = Contest.objects.all()
    return render(request, "cindex.html", {'contest_list': requested})

def contestpage(request):
    cid = request.GET.get('cid')
    requested = Contest.objects.filter(con_id = cid)
    target = requested[0]
    return render(request, "contestpage.html", {'contest': target})
    #如何显示存储的图片是个问题


# Create your views here.
