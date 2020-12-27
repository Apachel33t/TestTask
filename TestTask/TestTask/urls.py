from django.conf.urls import url
from testAPIService import views

urlpatterns = [
    url(r'^api/post$', views.PostView.post_list),
    url(r'^api/post/(?P<pk>[0-9]+)$', views.PostView.post_detail),
    url(r'^api/post/published$', views.PostView.post_list_published),
]