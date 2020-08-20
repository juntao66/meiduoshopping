from django.conf.urls import url, include
from django.contrib import admin
from . import  views
urlpatterns = [
    url(r'^register/$',  views.RegisterView.as_view()),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{4,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^login/$', views.LoginView.as_view(),  name='login'),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^info/$', views.UserInfoView.as_view(), name='info'),
    url(r'^email/$', views.EmailView.as_view()),
    url(r'^addresses/$', views.AddressView.as_view(), name='address'),
    url(r'^addresses/create/$', views.AddressCreateView.as_view()),
]