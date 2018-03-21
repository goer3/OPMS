########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.conf.urls import url
from opms_project import settings

########################################################################################################################
## 系统自带模块导入
########################################################################################################################
from .views import *

########################################################################################################################
## 自建模块导入
########################################################################################################################


########################################################################################################################
## url
########################################################################################################################
app_name = 'users'

urlpatterns = [
    # 首页
    url(r'^$', IndexView.as_view(), name='index'),

    # 用户登录
    url(r'^login/$', LoginView.as_view(), name='login'),

    # 用户注销登录
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    # 忘记密码
    url(r'^forget/$', ForgetPasswordView.as_view(), name='forget_password'),

    # 重置密码页面
    url(r'^reset/(?P<reset_code>.*)$', ResetPasswordView.as_view(), name='reset_password'),

    # 重置密码
    url(r'^modify/$', ModifyPasswordView.as_view(), name='modify_password'),

    # 用户信息
    url(r'^user/info/$', UserInfoView.as_view(), name='user_info'),

    # 修改头像
    url(r'^user/change/avatar/$', ChangeAvatarView.as_view(), name='change_avatar'),

    # 修改密码
    url(r'^user/change/password/$', ChangePasswordView.as_view(), name='change_password'),

    # 发送修改邮箱验证码
    url(r'^user/send/change_email_code/$', SendChangeEmailCodeView.as_view(), name='send_change_email_code'),

    # 修改邮箱
    url(r'^user/change/email/$', ChangeEmailView.as_view(), name='change_email'),

    # 其他用户信息
    url(r'^other/user/info/(?P<uid>\d+)$', OtherUserInfoView.as_view(), name='other_user_info'),

    # 登录记录
    url(r'^user/login/record/$', UserLoginRecordView.as_view(), name='login_record'),

    # 用户列表
    url(r'^user/list/$', UserListView.as_view(), name='user_list'),

    # 用户状态管理
    url(r'^user/mana/status/(?P<uid>\d+)$', UserStatusManaView.as_view(), name='user_status_mana'),
]


