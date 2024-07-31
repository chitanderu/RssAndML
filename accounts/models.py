from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser):
    email = models.CharField(unique=True,max_length=30)
    name = models.CharField(max_length=30)
    userpass=models.CharField(max_length=30,default='')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f'{self.name}'

    def get_short_name(self):

        return self.name

    def has_module_perms(self, app_label):
        return self.is_staff

class UserFeedInfo(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    link = models.CharField(max_length=255)
    img_src=models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField()
    pub_date = models.TextField()
    expert=models.TextField(default='')
    category=models.TextField(default='',null=True, blank=True)
    sourcename = models.TextField(default='',null=True, blank=True)
    url=models.CharField(default='',null=True, max_length=255)


    def __str__(self):
        return self.title

    def __lt__(self, other):
        """
        定义 UserFeedInfo 对象之间的小于关系，用于排序
        """
        return self.id < other.id

    # # 自定义 get_absolute_url 方法
    # # 记得从 django.urls 中导入 reverse 函数
    # def get_absolute_url(self):
    #     return reverse('headblog:detail', kwargs={'id': self.id})


    def __str__(self):
        return str(self.id)


class UserCommentInfo(models.Model):
    comment = models.TextField()
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post=models.ForeignKey(UserFeedInfo, on_delete=models.CASCADE)
    datatime=models.TextField()



    # # 自定义 get_absolute_url 方法
    # # 记得从 django.urls 中导入 reverse 函数
    # def get_absolute_url(self):
    #     return reverse('headblog:detail', kwargs={'id': self.id})


    def __str__(self):
        return str(self.id)

