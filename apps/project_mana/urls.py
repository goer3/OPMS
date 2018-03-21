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


app_name = 'project_mana'

########################################################################################################################
## url
########################################################################################################################
urlpatterns = [
    # 项目分类
    url(r'^category/$', ProjectCategoryView.as_view(), name='project_category'),

    # 添加项目分类
    url(r'^category/add/$', AddProjectCategoryView.as_view(), name='add_project_category'),

    # 管理项目分类
    url(r'^category/mana/$', ManaProjectCategoryView.as_view(), name='mana_project_category'),

    # 项目分类
    url(r'^category/(?P<cate_id>\d+)/project/list/$', ProjectListView.as_view(), name='project_list'),

    # 添加项目
    url(r'^category/(?P<cate_id>\d+)/project/add/$', AddProjectView.as_view(), name='add_project'),

    # 管理项目
    url(r'^category/(?P<cate_id>\d+)/project/(?P<pro_id>\d+)/mana/$', ManaProjectView.as_view(), name='mana_project'),

    # 项目详情
    url(r'^category/(?P<cate_id>\d+)/project/(?P<pro_id>\d+)/detail/$', ProjectDetailView.as_view(), name='project_detail'),

    # 项目文档
    url(r'^category/(?P<cate_id>\d+)/project/(?P<pro_id>\d+)/doc/$', ProjectInfoView.as_view(), name='project_info'),

    # 文档列表
    url(r'^install/doc/list/$', InstallDocListView.as_view(), name='install_doc_list'),

    # 文档详情
    url(r'^install/doc/detail/(?P<doc_id>\d+)/$', InstallDocDetailView.as_view(), name='install_doc_detail'),

    # 添加文档
    url(r'^install/doc/add/$', AddInstallDocView.as_view(), name='add_install_doc'),

    # 管理文档
    url(r'^install/doc/delete/$', ManaInstallDocView.as_view(), name='mana_install_doc'),

    # 修改文档
    url(r'^install/doc/change/(?P<doc_id>\d+)/$', ChangeInstallDocView.as_view(), name='change_install_doc'),
]



