from headblog import views


from django.urls import path, include


app_name = 'headblog'
urlpatterns = [

    path('',views.index),
    path('posts/<int:id>/', views.detail, name='detail'),
]
