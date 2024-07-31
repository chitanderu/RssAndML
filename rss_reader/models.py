from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils import timezone

class FeedInfo(models.Model):
    title = models.CharField(max_length=250)
    link = models.CharField(max_length=255)
    img_src=models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField()
    pub_date = models.TextField()
    expert=models.TextField(default='')
    category=models.TextField(default='',null=True, blank=True)
    sourcename = models.TextField(default='',null=True, blank=True)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('headblog:detail', kwargs={'id': self.id})


    def __str__(self):
        return str(self.id)



class Feedurl(models.Model):
     url= models.TextField(default='',null=True, blank=True)
     name=models.TextField(default='',null=True, blank=True)

     def __str__(self):
         return str(self.id)

