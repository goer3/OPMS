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

app_name = 'online_deploy'

########################################################################################################################
## url
########################################################################################################################
urlpatterns = [
    # 服务列表
    url(r'^list/service/$', ServiceListView.as_view(), name='service_list'),

    # 添加服务
    url(r'^service/add/$', AddServiceView.as_view(), name='add_service'),

    # 修改服务
    url(r'^service/change/(?P<s_id>\d+)/$', ChangeServiceView.as_view(), name='change_service'),

    # 中间件列表
    url(r'^list/middleware/$', MiddlewareRecordListView.as_view(), name='middleware_list'),

    # 添加中间件记录
    url(r'^middleware/add/$', AddMiddlewareView.as_view(), name='add_middleware'),

    # 修改记录
    url(r'^middleware/change/(?P<m_id>\d+)/$', ChangeMiddlewareView.as_view(), name='change_middleware'),

    # 删除记录
    url(r'^middleware/delete/(?P<m_id>\d+)/$', DeleteMiddlewareView.as_view(), name='delete_middleware'),

    # 产品发布列表
    url(r'^list/deploy/$', DeployRecordListView.as_view(), name='deploy_list'),

    # 添加发布记录
    url(r'^deploy/add/$', AddDeployRecordView.as_view(), name='add_deploy'),

    # 修改记录
    url(r'^deploy/change/(?P<d_id>\d+)/$', ChangeDeployRecordView.as_view(), name='change_deploy'),

    # 删除记录
    url(r'^deploy/delete/(?P<d_id>\d+)/$', DeleteDeployRecordView.as_view(), name='delete_deploy'),
]








