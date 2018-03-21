########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.conf.urls import url, include
from django.views.static import serve
from opms_project import settings

########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import xadmin

########################################################################################################################
## 自建模块导入
########################################################################################################################
from record.views import get_province, get_city, get_area
from project_mana.views import upload_image

########################################################################################################################
## 入口url
########################################################################################################################
urlpatterns = [
    # xadmin
    url(r'^xadmin/', xadmin.site.urls),

    # media 配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 用户url入口
    url(r'', include('users.urls')),

    # 用户消息入口
    url(r'^message/', include('message.urls')),

    # 验证码
    url(r'^captcha/', include('captcha.urls')),

    # 故障记录
    url(r'^record/', include('record.urls')),

    # 省市区
    url(r'^province/$', get_province, name='get_province'),
    url(r'^city_(?P<pid>\d+)/$', get_city, name='get_city'),
    url(r'^area_(?P<pid>\d+)/$', get_area, name='get_area'),

    # 项目管理
    url(r'^project/', include('project_mana.urls')),

    # CKeditor上传图片
    url(r'^uploadimg/', upload_image),

    # 查看图片路径
    url(r'^upload/ckeditor/image/(?P<path>(\S)*)', serve, {'document_root': settings.BASE_DIR + '/upload/ckeditor/image/'}),

    # 资产管理
    url(r'^asset/', include('asset.urls')),

    # 任务管理
    url(r'^task/', include('work_task.urls')),

    # 服务记录
    url(r'^deploy/', include('online_deploy.urls')),
]
