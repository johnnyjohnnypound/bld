from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$',views.index, name='index'),
        url(r'^add/$',views.add,name='add'),
        url(r'^user/(?P<cun>.+)/$',views.ud,name='ud'),
        url(r'^users/$',views.us,name='us'),
        url(r'^list/$',views.list,name='list')
        ]
