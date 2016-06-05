from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^init$', views.init),
    url(r'^rfsh$', views.rfsh),
    url(r'^chkDB$', views.chkDB),
    url(r'^set$', views.set),
    url(r'^setChk$', views.setChk),
    url(r'^game$', views.game),
    url(r'^wait$', views.wait),
    url(r'^deal$', views.deal)
]