from django.urls import path

from . import views

app_name = 'contest'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('contestpage/', views.contestpage, name='info'),
    path('addpost/', views.addpost, name='newpost'),
    path('search/', views.search, name='search'),
]