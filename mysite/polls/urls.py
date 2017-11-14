from django.conf.urls import url
from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.post_new, name='post_ad'),
    url(r'^results/$',views.post_list, name='results'),
]
