from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from aip import AipNlp
# Create your views here.
from django.shortcuts import render
import feedparser
from django.utils.html import strip_tags
from django.views import View
from bs4 import BeautifulSoup
from .models import FeedInfo

# def index(request):
#     # 获取订阅源数据
#     rss_url = 'https://rsshub.app/21caijing/channel/readnumber'
#     feed = feedparser.parse(rss_url)
#     #print(feed)
#     print(type(Feed))
#
#     entries = feed.entries
#
#     #print(entries)
#     # # 将数据存储到数据库中
#
#
#     for entry in entries:
#         feed = Feed(title=entry.title, link=entry.link, description=entry.description, pub_date=entry.title)
#         feed.save()
#
#     # 从数据库中获取数据并渲染到模板中
#     feeds = Feed.objects.all().order_by('-pub_date')
#
#
#     #feeds=feed.entries
#     context = {'feeds': feeds}
#     return render(request, 'headindex.html', context)



# #不用vue的方法
#     feed = feedparser.parse('https://rsshub.app/21caijing/channel/readnumber')
#     entries = feed.entries
#     items = []
#
#     for entry in entries:
#         item = {}
#         item['title'] = entry.title
#         item['description'] = entry.description
#         item['link'] = entry.link
#         item['pub_date'] = entry.title
#         soup = BeautifulSoup(item['description'], features="html.parser")
#
#         item['description'] = soup.get_text()
#         items.append(item)
#     context = {'feeds': items}
#     #print(context)
#     return render(request, 'headindex.html', context)
from datetime import datetime
from rss_reader.models import FeedInfo


class RSSViewsql(View): #类视图用来处理json 发起请求


    def get(self, request):

                #循环取值
            all_feed_info = FeedInfo.objects.all()
            sqlitem=[]
            for single in all_feed_info:
                    sqlitem.append({
                        'title': single.title,
                        'description': single.description,
                        'pub_date': single.pub_date,
                        'link':single.link,
                        'img_src':single.img_src,
                        'category':single.category,
                        'expert': single.expert,
                         'id':single.id
                        # 将其他需要的属性也加入字典中
                    })








            return JsonResponse(sqlitem, safe=False)