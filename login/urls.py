from django.contrib import admin
from django.urls import path
from django.urls import path, include
from  login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rss_reader/', include('rss_reader.urls')),
    path('',views.index1),



]
