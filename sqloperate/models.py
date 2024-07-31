from django.db import models

# Create your models here.
from django.db import models

class FeedInfo(models.Model):
    title = models.CharField(max_length=250)
    link = models.CharField(max_length=255)
    img_src=models.CharField(max_length=255)
    description = models.TextField()
    pub_date = models.TextField()
    expert=models.TextField(default='')
    category=models.TextField(default='')





    def __str__(self):
        return str(self.id)

