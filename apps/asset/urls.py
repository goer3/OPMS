########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.conf.urls import url, include
from django.views.static import serve
from opms_project import settings

########################################################################################################################
## 系统自带模块导入
########################################################################################################################


########################################################################################################################
## 自建模块导入
########################################################################################################################
from .views import *


app_name = 'asset'

########################################################################################################################
## url
########################################################################################################################
urlpatterns = [
    # 用户反馈
    url(r'^host/list/$', HostListView.as_view(), name='host_list'),

    # 添加记录
    url(r'^host/add/$', AddHostView.as_view(), name='add_host'),

    # 修改记录
    url(r'^host/change/(?P<h_id>\d+)/$', ChangeHostView.as_view(), name='change_host'),

    # 删除记录
    url(r'^host/delete/(?P<h_id>\d+)/$', DeleteHostView.as_view(), name='delete_host'),

    # webssh
    url(r'^host/webssh/(?P<serv_id>\d+)/$', WebSSHView.as_view(), name='web_ssh'),

    # webssh记录
    url(r'^host/webssh/history/$', WebSSHListView.as_view(), name='ssh_history_list'),

    # 端口映射
    url(r'^port/map/list/$', PortMapListView.as_view(), name='port_map_list'),

    # 添加端口映射
    url(r'^port/map/add/$', AddPortMapView.as_view(), name='add_port_map'),

    # 删除映射记录
    url(r'^port/delete/(?P<p_id>\d+)/$', DeletePortMapView.as_view(), name='delete_port'),

    # 修改映射记录
    url(r'^port/map/change/(?P<p_id>\d+)/$', ChangePortMapView.as_view(), name='change_port'),
]



