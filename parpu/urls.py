"""parpu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect, HttpResponse

def login(request):
    """
    process the users' login
    """
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        #用户 post 时提交的数据，读取
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        if email == "duanzj" and pwd == "123" :
            # login successed
            return redirect('/personalpage/')
        else:
            # login failed
            return render(request, "login.html", {'msg': "Invalid username or password"})

def personalpage(request):
    """
    进入用户中心
    """
    return render(request, "personalpage.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('personalpage/', personalpage),
]
