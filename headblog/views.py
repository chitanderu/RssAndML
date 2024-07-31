from django.shortcuts import render, get_object_or_404
from  accounts.models import  MyUser
from  rss_reader.models import FeedInfo
# Create your views here.
def index(request):
    #username = request.GET.get('username', None)  #临时name
    username = request.session.get('username')
    user = MyUser.objects.get(name=username)
    user_id = user.id
    page=1




    return render(request, "headindex.html", {'username': username,'user_id':user_id,'page':page})



def detail(request, id):
    post = get_object_or_404(FeedInfo, id=id)

    print(post)
    return render(request, 'detail.html', context={'post': post})