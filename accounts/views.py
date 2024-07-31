from datetime import datetime
import feedparser
from aip import AipNlp
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
import feedparser
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from numpy import sort
from pywebio.platform.django import webio_view

from .models import UserFeedInfo
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import MyLoginForm, MyRegistrationForm, RSSFeedForm
from django.contrib.auth import get_user_model
from .models import MyUser, UserFeedInfo
from django.core.exceptions import ValidationError
from rss_reader.models import Feedurl
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
def login_view(request):



    if request.method == 'POST':
        form = MyLoginForm(request=request, data=request.POST)

        form.is_valid()
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(email + password)
        if email and password:
            user = MyUser.objects.filter(email=email, userpass=password).first()
        if user is not None:
            login(request, user)
            request.session['username'] = user.name
            return HttpResponseRedirect('/headblog/?username={}'.format(user.name))
        else:

            print("no!!!")
            print(form.errors)
    else:
        form = MyLoginForm()
    return render(request, 'login.html', {'form': form})


# def login_view(request):
#     User = get_user_model()
#     print(User)
#     if request.method == 'POST':
#         form = MyLoginForm(request=request, data=request.POST)
#
#         if form.is_valid():
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             print(type(email))
#             user = MyUser.objects.filter(email=email)
#
#             print(user.name)
#
#             # user = authenticate(request=request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('/headblog')
#         else:
#             # email = form.cleaned_data.get('username')
#             # password = form.cleaned_data.get('password')
#             # user = MyUser.objects.filter(email=email, userpass=password)
#             # single = user.first()
#             # if user is not None:
#             #     print(single.name)
#             #     login(request, single)
#             #     return redirect('/headblog')
#             #
#             # else:
#             print(form.errors)
#     else:
#         form = MyLoginForm()
#     return render(request, 'login.html', {'form': form})
from rss_reader.models import Feedurl
def remove_emoji(string):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r'', string)


def clean_text(text):
    # 只保留中文或英文字符
    pattern = re.compile('[^\u4e00-\u9fa5a-zA-Z]')
    return pattern.sub('', text)
@login_required
def rss_list(request, username,page):


    allurl=Feedurl.objects.all()

    global all_feed_info, sqlitem, url
    APP_ID = '30610004'
    API_KEY = '6gT4lh7DtMW07DQ5cpdpwADC'
    SECRET_KEY = 'N399OPRIYdIBuu92psGcyHYCMnim9GiT'
    users = MyUser.objects.filter(name=username)
    user = users.first()
    id = user.id
    print("USERID"+str(id))
    name=user.name
    categories = []
    source=[]
    # 获取当前用户添加的所有 rss
    rss_feeds =  UserFeedInfo.objects.filter(user=id)[::-1]
    for s in rss_feeds:
        categories.append(s.category)
        source.append(s.sourcename)


    categories=set(categories)
    if " " in categories:
        categories.remove(" ")

    source=set(source)

    rss_feeds = UserFeedInfo.objects.filter(user_id=id)
    category_counts = rss_feeds.exclude(category=" ").values('category').annotate(count=Count('category')).order_by(
        # 统计这些 RSS 源的分类，并按照分类的订阅数量从大到小排序
        '-count')
    top_categories = [c['category'] for c in category_counts[:2]]
    recommended_feeds = UserFeedInfo.objects.filter(category__in=top_categories).order_by('?')[:5]  # 找到订阅数量最多的两个分类
    # 从这两个分类中随机选择一个 RSS 源，并推荐给用户



     # print(categories)
    #获取当前用户的所有标签
    #实现分页

    rss_feeds = UserFeedInfo.objects.filter(user=id)[::-1]
    paginator=Paginator(rss_feeds,10)
    page_obj = paginator.get_page(page)

    #page = request.GET.get('page')
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        feeds = paginator.page(1)
    except EmptyPage:
        feeds = paginator.page(paginator.num_pages)









    if request.method == 'POST':
        form = RSSFeedForm(request.POST)

        form.is_valid()
        # rss_feed = form.save(commit=False)

        url = form.cleaned_data['url']
        print(url)
        feed = feedparser.parse(url)
        entries = feed.entries
        items = []
        for entry in entries:
            item = {}
            item['title'] = entry.title
            item['description'] = entry.description
            item['link'] = entry.link
            currentDateAndTime = datetime.now()
            item['pub_date'] = currentDateAndTime
            item['sourcename'] = feed['feed']['title']
            item['url'] = url
            item['user'] = id
            soup1 = BeautifulSoup(entry.description, features='html.parser')
            # print(type(entry.ti tle))
            img_src = "https://pic.imgdb.cn/item/64087ba7f144a01007bfecf0.png"  # 给变量 img_src 赋一个默认值 None

            img_tag = soup1.find('img')
            if img_tag:
                img_src = img_tag['src']
                # print('Image:', img_src)
            else:
                pass
                # print('Image not found')
            item['img'] = img_src

            soup = BeautifulSoup(item['description'], features="html.parser")
            item['description'] = soup.get_text()
            item['description']=clean_text(item['description'])
            summary = '。'.join(item['description'].split('。')[:1]) + '。'
            item['expert'] = summary
            client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
            item['category'] = " "
            tag = client.topic(entry.title, item['description'])
            tag_item = tag.get('item')
            if tag_item:
                lv1_tag_list = tag_item.get('lv1_tag_list')
                if lv1_tag_list:
                    try:
                        item['category'] = tag['item']['lv1_tag_list'][0]['tag']
                    except KeyError:
                        print("Category not found in tag.")
                        item['category'] = " "

            with transaction.atomic():
                sqlitem = UserFeedInfo(title=entry.title, link=entry.link, img_src=item['img'],
                                       description=soup.get_text(),
                                       pub_date=currentDateAndTime, expert=item['expert'], category=item['category'],
                                       sourcename=item['sourcename'], user_id=id, url=url)
                if UserFeedInfo.objects.filter(title=entry.title, user_id=id):
                    my = UserFeedInfo.objects.filter(title=entry.title)
                    for mysingle in my:
                        pass
                        # print("已经存在"+mysingle.title)
                    pass
                else:
                    sqlitem.save()




            items.append(item)

        # rss_feed.user = request.user.id
        # rss_feed.save()

        # messages.success(request, 'RSS feed added successfully.')
        return redirect(reverse('accounts:rss_list', kwargs={'username': name,'page':1}))

    else:
        form = RSSFeedForm()

    return render(request, 'rss_list.html', {'page_obj': page_obj,'rss_feeds': feeds, 'form': form, 'id': id,'username':name,'page': page,'category':categories,'source':source,'topcate':top_categories,'recommend':recommended_feeds ,'allurl':allurl,'user':user})


@login_required
def rss_refresh(request, rss_id):
    rss_feed = UserFeedInfo.objects.get(id=rss_id)
    rss_feed.refresh()

    # messages.success(request, 'RSS feed refreshed successfully.')
    return redirect(reverse('rss_list'))


def register_view(request):
    if request.method == 'POST':
        # 获取用户提交的表单数据
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # 验证用户是否已经存在
        if MyUser.objects.filter(email=email).exists() or MyUser.objects.filter(name=name).exists():
            messages.error(request, '该邮箱或用户名已经存在')
            return redirect('accounts:register')

        # 创建新用户
        user = MyUser(email=email, name=name,userpass=password,last_login="2022-10-21",is_active=True,is_staff=False)
        user.set_password(password)
        user.save()

        messages.success(request, '注册成功！请登录')
        return redirect('accounts:login')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('home')

from .models import  UserCommentInfo
def detail(request,id,username):
    post = get_object_or_404(UserFeedInfo, id=id)
    APP_ID = '31211181'
    API_KEY = 'LQeqioGoHHdQRUYQM86XL6wY'
    SECRET_KEY = 'OP03r0PeW3OPQM58LhuwvInOYXXhCEH4'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    dec=post.description
    tit=post.title
    tdata=[]
    keytopic=client.keyword(tit,dec)
    alltopic = keytopic.get("items")
    if alltopic:
        for s in alltopic:
            tdata.append(s['tag'])

    users = MyUser.objects.filter(name=username)
    user = users.first()
    uid = user.id
    uname=user.name
    print(uid)
    postid=id
    #print(post)
    i=0
    allcomment=UserCommentInfo.objects.filter(user_id=uid,post_id=postid)
    print(allcomment)
    for single in allcomment:
        print(single.comment)
        i+=1

    users = MyUser.objects.filter(name=username)
    user = users.first()
    uid = user.id

    name = username

    pid = id
    if request.method == 'POST':
        comment = request.POST['comment']
        currentDateAndTime = datetime.now()
        nowtime = currentDateAndTime
        # user = MyUser(email=email, name=name,userpass=password,last_login="2022-10-21",is_active=True,is_staff=False)
        sqlitem = UserCommentInfo(post_id=pid, user_id=uid, datatime=nowtime, comment=comment)
        sqlitem.save()
        return redirect(reverse('accounts:detail',kwargs={'username': name, 'id': pid}) )

    print(i)
    return render(request, 'userdetail.html', context={'post': post,'comments':allcomment,'count':i,'uid':uid,'username':uname,'keytopic':tdata})




import feedparser
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import UserFeedInfo

@require_GET
def refresh_rss(request, username):
    global all_feed_info, sqlitem, url
    APP_ID = '30610004'
    API_KEY = '6gT4lh7DtMW07DQ5cpdpwADC'
    SECRET_KEY = 'N399OPRIYdIBuu92psGcyHYCMnim9GiT'
    subscriptions = UserFeedInfo.objects.filter(user__name=username)
    sources = list(set(subscriptions.values_list('url', flat=True)))
    users = MyUser.objects.filter(name=username)
    user = users.first()
    id = user.id
    name = user.name
    items = []
    print(sources)
    for url in sources:
        feed = feedparser.parse(url)
        entries = feed.entries




        for entry in entries:
            item = {}
            item['title'] = entry.title
            item['description'] = entry.description
            item['link'] = entry.link
            currentDateAndTime = datetime.now()
            item['pub_date'] = currentDateAndTime
            item['sourcename'] = feed['feed']['title']
            item['url'] = url
            item['user'] = id
            soup1 = BeautifulSoup(entry.description, features='html.parser')
            # print(type(entry.ti tle))
            img_src = "https://pic.imgdb.cn/item/64087ba7f144a01007bfecf0.png"  # 给变量 img_src 赋一个默认值 None

            img_tag = soup1.find('img')
            if img_tag:
                img_src = img_tag['src']
                # print('Image:', img_src)
            else:
                pass
                # print('Image not found')
            item['img'] = img_src

            soup = BeautifulSoup(item['description'], features="html.parser")
            item['description'] = soup.get_text()
            summary = '。'.join(item['description'].split('。')[:1]) + '。'
            item['expert'] = summary
            client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
            item['category'] = " "
            tag = client.topic(entry.title, item['description'])
            tag_item = tag.get('item')
            if tag_item:
                lv1_tag_list = tag_item.get('lv1_tag_list')
                if lv1_tag_list:
                    try:
                        item['category'] = tag['item']['lv1_tag_list'][0]['tag']
                    except KeyError:
                        print("Category not found in tag.")
                        item['category'] = " "

            with transaction.atomic():
                sqlitem = UserFeedInfo(title=entry.title, link=entry.link, img_src=item['img'],
                                       description=soup.get_text(),
                                       pub_date=currentDateAndTime, expert=item['expert'], category=item['category'],
                                       sourcename=item['sourcename'], user_id=id, url=url)
                if UserFeedInfo.objects.filter(title=entry.title, user_id=id):
                    my = UserFeedInfo.objects.filter(title=entry.title)
                    for mysingle in my:
                        pass
                        # print("已经存在"+mysingle.title)
                    pass
                else:
                    sqlitem.save()
                    items.append(item)



    # for source in sources:
    #     feed = feedparser.parse(source)
    #     for item in feed.entries:
    #         # 处理每一篇 RSS 订阅的条目，将其转换成 Item 模型并保存
    #         # 注意需要根据 item 的内容去重，避免重复保存
    #         # 将成功保存的条目添加到 updated_items 列表中





    #print(items)
    # 判断是否有更新，如果有则发送 success message
    # if items:
    #     messages.success(request, f"成功刷新 {len(items)} 条订阅")

    # 返回更新成功的条目数，以便前端渲染
    print("CHANGDU"+ str(len(items)))
    return JsonResponse({'updated_items': len(items)})




def rss_archive(request, username,page):
    user = MyUser.objects.filter(name=username).first()
    if user is None:
        raise Http404("User does not exist")

    feed_info = UserFeedInfo.objects.filter(user=user.id) \
        .values('sourcename') \
        .annotate(total=Count('sourcename')) \
        .order_by('-total')

    article_groups = []
    for info in feed_info:
        sourcename = info['sourcename']
        articles = UserFeedInfo.objects.filter(user=user.id, sourcename=sourcename) \
            .order_by('-pub_date') \
            .values('id','title', 'link', 'expert')
        #print(articles)
        article_groups.append({'sourcename': sourcename, 'articles': articles})

    #print(type(article_groups))
    #print(article_groups)
    aid=[]
    for group in article_groups:
        for s in group['articles']:
            #print(s['id'])
            aid.append(s['id'])

    context = {
        'user': user,
        'article_groups': article_groups,
        'username': user.name,
        'rss_id':user.id,



    }
    return render(request, 'rss_archive.html', context)



from django.shortcuts import render


from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./accounts/templates"))
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import  Grid
#https://pyecharts.org/#/zh-cn/rectangular_charts
def data(request,username):
    users = MyUser.objects.filter(name=username)
    user = users.first()
    id = user.id
    print("USERID" + str(id))
    name = user.name
    categories = []
    source = []
    rss_feeds = UserFeedInfo.objects.filter(user_id=id)
    category_counts = rss_feeds.exclude(category=" ").values('category').annotate(count=Count('category')).order_by(  # 统计这些 RSS 源的分类，并按照分类的订阅数量从大到小排序
        '-count')
    top_categories = [c['category'] for c in category_counts[:2]]  # 找到订阅数量最多的两个分类
    recommended_feeds = UserFeedInfo.objects.filter(category__in=top_categories).order_by('?')[:5]    # 找到订阅数量最多的两个分类
    # 从这两个分类中随机选择一个 RSS 源，并推荐给用户



    # 获取当前用户添加的所有 rss
    rss_feeds = UserFeedInfo.objects.filter(user=id)
    category_counts = rss_feeds.exclude(category=" ").values('category').annotate(count=Count('category'))
    category_counts_list = list(category_counts.values_list('category','count' ))
    print(category_counts_list)
    categories = set(categories)
    if " " in categories:
        categories.remove(" ")
    c = (
        Bar()
        .add_xaxis([x[0] for x in category_counts_list])
        .add_yaxis(user.name, [x[1] for x in category_counts_list])
        .set_global_opts(title_opts=opts.TitleOpts(title="订阅文章类型分析", subtitle="来自所有rss"),
            datazoom_opts=opts.DataZoomOpts(),  )
    )
    # p=(
    #     Pie()
    #         .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
    #         .add("", category_counts_list)
    #         .set_global_opts(title_opts=opts.TitleOpts(title="饼图分析"))
    #
    #
    #
    #
    # )

    print(top_categories[0])
    chart_html = c.render_embed()
    context = {
         "tag": top_categories,
        "chart": chart_html,
    }
    return HttpResponse(c.render_embed(kwargs={'alltag': top_categories }))



import random
import pyecharts.options as opts
from pyecharts.charts import WordCloud
import json
import re
from pyecharts.charts import Pie
from collections import Counter
from rss_reader.models import Feedurl
def clean_text(text):
    # 只保留中文或英文字符
    pattern = re.compile('[^\u4e00-\u9fa5a-zA-Z]')
    return pattern.sub('', text)
def cloud(request,username):
    normalrss=Feedurl.objects.all()

    APP_ID = '31211181'
    API_KEY = 'LQeqioGoHHdQRUYQM86XL6wY'
    SECRET_KEY = 'OP03r0PeW3OPQM58LhuwvInOYXXhCEH4'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    users = MyUser.objects.filter(name=username)
    user = users.first()
    id = user.id
    print("USERID" + str(id))
    user_feeds = UserFeedInfo.objects.filter(user_id=id)

    # 如果UserFeedInfo对象数量不足50，则获取所有对象
    if len(user_feeds) <= 49:
        selected_user_feeds = user_feeds
    else:
        # 随机选取50个UserFeedInfo对象
        selected_user_feeds = random.sample(sorted(user_feeds), 50)

    data1 = [(clean_text(feed.title), clean_text(feed.expert)) for feed in selected_user_feeds] ## 提取title和description字段，并保存在一个列表中
    #print(data1)
    tdata=[]
    for singledata in data1:
        print(singledata[0])
        topic=client.keyword( singledata[0],singledata[1] )
        alltopic=topic.get("items")
        if alltopic:
            for s in alltopic:
                tdata.append(s['tag'])

    print(tdata[0])
    tdata_count = Counter(tdata)

    tdata_with_count = [(key, value) for key, value in tdata_count.items()]
    print(tdata_with_count)








    data = [

        ("公交运输管理", "11"),
        ("公路（水路）交通", "11"),
        ("房屋与图纸不符", "11"),
        ("有线电视", "11"),
        ("社会治安", "11"),
        ("林业资源", "11"),
        ("其他行政事业收费", "11"),
        ("经营性收费", "11"),
        ("食品安全与卫生", "11"),
        ("体育活动", "11"),
        ("有线电视安装及调试维护", "11"),
        ("低保管理", "11"),
        ("劳动争议", "11"),
        ("社会福利及事务", "11"),
        ("一次供水问题", "11"),
    ]

    c=(
        WordCloud(init_opts=opts.InitOpts(width="1700px",
                                height="750px",
                                page_title="rss词云",
                                 ))
             .add(series_name="热点分析", data_pair= tdata_with_count, word_size_range=[6, 66],shape="cirlce",)
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23),



            ),
            tooltip_opts=opts.TooltipOpts(is_show=True,),
        )

    )
    return HttpResponse(c.render_embed())






def deleterss(request,username,sourcename):
    if request.method == 'POST':
         dname=username
         dsource=sourcename
         users = MyUser.objects.filter(name=username)
         user = users.first()
         uid = user.id
         UserFeedInfo.objects.filter(user_id=uid, sourcename=dsource).delete()
         return redirect('accounts:rss_list', username=username, page=1)


def addthisurl(request,username,url_id):

    if request.method == 'POST':
        APP_ID = '30610004'
        API_KEY = '6gT4lh7DtMW07DQ5cpdpwADC'
        SECRET_KEY = 'N399OPRIYdIBuu92psGcyHYCMnim9GiT'
        name = username
        thisurl=Feedurl.objects.filter(id=url_id).first()
        url=thisurl.url
        print("默认列表的url")
        print(url)

        users = MyUser.objects.filter(name=username)
        user = users.first()
        id = user.id

        feed = feedparser.parse(url)
       # print(feed)
        entries = feed.entries
        items = []
        for entry in entries:
            item = {}
            item['title'] = entry.title
            item['description'] = entry.description
            item['link'] = entry.link
            currentDateAndTime = datetime.now()
            item['pub_date'] = currentDateAndTime
            item['sourcename'] = feed['feed']['title']
            item['url'] = url
            item['user'] = id
            soup1 = BeautifulSoup(entry.description, features='html.parser')
            # print(type(entry.ti tle))
            img_src = "https://pic.imgdb.cn/item/64087ba7f144a01007bfecf0.png"  # 给变量 img_src 赋一个默认值 None

            img_tag = soup1.find('img')
            if img_tag:
                img_src = img_tag['src']
                # print('Image:', img_src)
            else:
                pass
                # print('Image not found')
            item['img'] = img_src

            soup = BeautifulSoup(item['description'], features="html.parser")
            item['description'] = soup.get_text()
            summary = '。'.join(item['description'].split('。')[:1]) + '。'
            item['expert'] = summary
            client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
            item['category'] = " "
            tag = client.topic(entry.title, item['description'])
            tag_item = tag.get('item')
            if tag_item:
                lv1_tag_list = tag_item.get('lv1_tag_list')
                if lv1_tag_list:
                    try:
                        item['category'] = tag['item']['lv1_tag_list'][0]['tag']
                    except KeyError:
                        print("Category not found in tag.")
                        item['category'] = " "

            with transaction.atomic():
                sqlitem = UserFeedInfo(title=entry.title, link=entry.link, img_src=item['img'],
                                       description=soup.get_text(),
                                       pub_date=currentDateAndTime, expert=item['expert'], category=item['category'],
                                       sourcename=item['sourcename'], user_id=id, url=url)
                if UserFeedInfo.objects.filter(title=entry.title, user_id=id):
                    my = UserFeedInfo.objects.filter(title=entry.title)
                    for mysingle in my:
                        pass
                        # print("已经存在"+mysingle.title)
                    pass
                else:
                    print("存储中")
                    sqlitem.save()

            items.append(item)

        # rss_feed.user = request.user.id
        # rss_feed.save()

        # messages.success(request, 'RSS feed added successfully.')
        return redirect(reverse('accounts:rss_list', kwargs={'username': username, 'page': 1}))
    return redirect(reverse('accounts:rss_list', kwargs={'username': username, 'page': 1}))



def  detailtag(request,username,tag):
    user = MyUser.objects.filter(name=username).first()
    if user is None:
        raise Http404("User does not exist")

    articles = UserFeedInfo.objects.filter(user_id=user.id, category=tag).order_by('-pub_date')
    context = {
        'user': user,
        'tag': tag,
        'articles': articles,
        'username': user.name
    }
    return render(request, 'tagarchive.html', context)


def  adminop(request):
     alluser=MyUser.objects.all()

     return render(request, 'admin.html',context={'alluser': alluser})


def  deleteuser(request,username):
    if request.method == 'POST':
        user_to_delete = MyUser.objects.filter(name=username)
        user_to_delete.delete()

        return redirect('accounts:uadmin')


    return render(request, 'admin.html')












