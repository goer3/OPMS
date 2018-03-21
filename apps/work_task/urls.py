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

app_name = 'work_task'

########################################################################################################################
## url
########################################################################################################################
urlpatterns = [
    # 接受任务
    url(r'^list/recive/$', UnfinishReceiveTaskListView.as_view(), name='receive_task_list'),

    # 创建任务
    url(r'^add/$', AddTaskView.as_view(), name='add_task'),

    # 终止任务
    url(r'^stop/(?P<t_id>\d+)/$', StopTaskView.as_view(), name='stop_task'),

    # 完结任务
    url(r'^finish/(?P<t_id>\d+)/$', FinishTaskView.as_view(), name='finish_task'),

    # 创建任务列表
    url(r'^list/create/$', CreateTaskListView.as_view(), name='create_task_list'),

    # 自己终止任务
    url(r'^create_user/stop/(?P<t_id>\d+)/$', CreateUserStopTaskView.as_view(), name='create_user_stop_task'),

    # 自己完结任务
    url(r'^create_user/finish/(?P<t_id>\d+)/$', CreateUserFinishTaskView.as_view(), name='create_user_finish_task'),

    # 修改任务
    url(r'^change/(?P<t_id>\d+)/$', ChangeTaskView.as_view(), name='change_task'),

    # 完结任务
    url(r'^list/finish/$', FinishTaskListView.as_view(), name='finish_task_list'),

    # 激活任务
    url(r'^active/(?P<t_id>\d+)/$', ActiveTaskView.as_view(), name='active_task'),
]












