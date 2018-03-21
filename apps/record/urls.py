########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.conf.urls import url
from django.views.static import serve
from opms_project import settings

########################################################################################################################
## 系统自带模块导入
########################################################################################################################

########################################################################################################################
## 自建模块导入
########################################################################################################################
from .views import *

########################################################################################################################
## url
########################################################################################################################

app_name = 'record'

urlpatterns = [
    # 记录列表
    url(r'^list/$', RecordListView.as_view(), name='record_list'),

    # 添加记录
    url(r'^add/record/$', AddRecordView.as_view(), name='add_record'),

    # 修改记录
    url(r'^change/record/$', ChangeRecordView.as_view(), name='change_record'),

    # 记录分类归档
    url(r'^archive/$', RecordArchiveView.as_view(), name='record_archive'),

    # 记录时间归档
    url(r'^archive/time/(?P<year>\d+)/(?P<month>\d+)/$', RecordTimeArchiveView.as_view(), name='record_time_archive'),

    # 记录标签归档
    url(r'^archive/tag/(?P<pid>\d+)/$', RecordTagArchiveView.as_view(), name='record_tag_archive'),

    # 记录省份归档
    url(r'^archive/province/(?P<pid>\d+)/$', RecordProvinceArchiveView.as_view(), name='record_province_archive'),

    # 记录用户归档
    url(r'^archive/user/(?P<pid>\d+)/$', RecordUserArchiveView.as_view(), name='record_user_archive'),
]