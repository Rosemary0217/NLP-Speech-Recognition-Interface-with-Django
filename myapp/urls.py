from django.urls import path
from django.urls import re_path
from . import views 
from django.conf.urls import include
from mytestsite import views as view1

urlpatterns = [
path("",views.index_in,name="index"),
#文件上传路由配置
path("upload",views.upload,name="upload"),#加载文件上传表单页
path("doupload",views.doupload,name="doupload"),#执行文件上传表单
path('settime', views.settime,name="settime"),           #修改录音时间
#path("output",views.doupload ,name="output"),#执行文件上传表单
path("monitor",views.monitor ,name="monitor"),#执行录音表单
path("output", view1.index_out,name="output"), #页面显示函数
path("monitors",views.monitors ,name="monitors"),#执行录音表单



]