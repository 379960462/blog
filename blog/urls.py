from django.conf.urls import url

from . import views
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),#归档
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),#分类页面
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),#获取某个标签下的文章列表
    url(r'^search/$', views.search, name='search'),#全文搜索
]