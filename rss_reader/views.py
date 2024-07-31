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


class RSSView(View): #类视图用来处理json 发起请求


    def get(self, request):
        """ 你的 APPID AK SK """
        global all_feed_info, sqlitem
        APP_ID = '30610004'
        API_KEY = '6gT4lh7DtMW07DQ5cpdpwADC'
        SECRET_KEY = 'N399OPRIYdIBuu92psGcyHYCMnim9GiT'
        urls=[ 'https://rsshub.app/huanqiu/news/china']

        for url in urls:
            feed = feedparser.parse(url)
            entries = feed.entries
           # print(entries[0])
            items = []
            for entry in entries:
                item = {}
                item['title'] = entry.title
                item['description'] = entry.description
                item['link'] = entry.link
                currentDateAndTime = datetime.now()
                item['pub_date'] =currentDateAndTime
                item['sourcename']=feed['feed']['title']
                soup1 = BeautifulSoup(entry.description, features='html.parser')
                #print(type(entry.ti tle))
                img_src = "https://pic.imgdb.cn/item/641287fbebf10e5d5303e0e6.jpg"  # 给变量 img_src 赋一个默认值 None



                img_tag = soup1.find('img')
                if img_tag:
                    img_src = img_tag['src']
                    #print('Image:', img_src)
                else:
                    pass
                    #print('Image not found')
                item['img']=img_src


                soup = BeautifulSoup(item['description'], features="html.parser")
                item['description'] = soup.get_text()
                summary = '。'.join(item['description'].split('。')[:1]) + '。'
                item['expert']=summary
                client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
                item['category'] = " "
                tag=client.topic(entry.title, item['description'])
                tag_item = tag.get('item')
                if tag_item:
                    lv1_tag_list = tag_item.get('lv1_tag_list')
                    if lv1_tag_list:
                        try:
                            item['category'] = tag['item']['lv1_tag_list'][0]['tag']
                        except KeyError:
                            print("Category not found in tag.")
                            item['category'] = ""
                #item['category']=tag['item']['lv1_tag_list'][0]['tag']
                #tagitem=FeedTag()








                with transaction.atomic():
                    sqlitem=FeedInfo(title=entry.title,link=entry.link,img_src=item['img'],  description=soup.get_text(),pub_date=currentDateAndTime,expert=item['expert'],category=item['category'],sourcename=item['sourcename'])
                    if FeedInfo.objects.filter(title=entry.title):
                     my=FeedInfo.objects.filter(title=entry.title)
                     for mysingle in my:
                         pass
                         #print("已经存在"+mysingle.title)
                     pass
                    else:
                     sqlitem.save()



               # 遍历所有对象，获取对应的属性值
                # for feed_info in all_feed_info:
                #         print(feed_info.id, feed_info.title, feed_info.link, feed_info.img_src, feed_info.description,
                #               feed_info.pub_date)







            items.append(item)
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
                        'sourcename': single.sourcename
                        # 将其他需要的属性也加入字典中
                    })








        return JsonResponse(sqlitem, safe=False)