from django.urls import path
from pywebio.platform.django import webio_view

from .views import login_view, register_view, logout_view
from . import  views

app_name = 'accounts'
#from pywebio.platform.django import webio_view
from django.urls import path


urlpatterns = [
    path('', login_view,name='login'),
    #path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    #path('headblog/', views.index),
    path('rss_list/<username>/<int:page>/', views.rss_list, name='rss_list'),
    path('rss_refresh/<int:rss_id>/', views.rss_refresh, name='rss_refresh'),
    path('rss_list/<username>/posts/<int:id>/',views.detail, name='detail'),
    path('refresh_rss/<username>/', views.refresh_rss, name='refresh_rss'),
    path('<str:username>/archive/<int:page>/',views.rss_archive,name='rss_archive'),
    path('data/<username>', views.data,name='data'),
    path('wordcloud/<username>', views.cloud, name='wordcloud'),
    path('rss_list/<username>/<sourcename>/', views.deleterss, name='delete'),
    path('rss_refresh/<username>/<int:url_id>/', views.addthisurl, name='add'),
    path('<str:username>/archive/<str:tag>/', views.detailtag, name='tag_archive'),
    path('uadmin/',  views.adminop, name='uadmin'),
    path('deleteadmin/<str:username>',  views.deleteuser, name='udelete'),


]