from django.urls import path

from . import views
from .views import RSSViewsql
app_name = 'myapp'
urlpatterns = [
     #path('', views.index, name='index'),#不用vue的方法
     path('', RSSViewsql.as_view(), name='rss'),]
