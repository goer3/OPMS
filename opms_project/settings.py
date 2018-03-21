"""
Django version: 1.11.8.
"""
import pymysql
pymysql.install_as_MySQLdb()

import os
import sys

########################################################################################################################
## 项目相关目录配置
########################################################################################################################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
## 自建APP
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
## 第三方APP
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


########################################################################################################################
## 安全配置
########################################################################################################################
SECRET_KEY = '(+!s-i*m=2oo9(yf)+)u&e9fd$jpvctwg9=sy1755l*2#b4+-_'

DEBUG = False
ALLOWED_HOSTS = ['*']


########################################################################################################################
## APP注册配置
########################################################################################################################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 用户
    'users',
    # xadmin
    'xadmin',
    'crispy_forms',
    # 用户消息
    'message',
    # 验证码
    'captcha',
    # 分页
    'pure_pagination',
    # 故障记录
    'record',
    # 项目文档管理
    'project_mana',
    # 资产管理
    'asset',
    # 任务管理
    'work_task',
    # 线上环境
    'online_deploy',
]


########################################################################################################################
## 中间件配置
########################################################################################################################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


########################################################################################################################
## 默认url入口文件配置
########################################################################################################################
ROOT_URLCONF = 'opms_project.urls'


########################################################################################################################
## 模板文件配置
########################################################################################################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Media 配置
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'opms_project.wsgi.application'


########################################################################################################################
## 数据库配置
########################################################################################################################
# 测试
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'opms_test',
        'HOST': '192.168.200.192',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456',
    }
}

########################################################################################################################
## 用户认证配置
########################################################################################################################
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


## 定义认证模型
AUTH_USER_MODEL = 'users.UserProfile'


# 邮箱登陆
AUTHENTICATION_BACKENDS = (
    'users.views.OtherLoginBackends',
)


########################################################################################################################
## 初始化配置
########################################################################################################################
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False


########################################################################################################################
## 静态文件配置
########################################################################################################################
# STATIC_ROOT = os.path.join(BASE_DIR, 'common_static').replace('\\','/')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


########################################################################################################################
## 上传文件配置
########################################################################################################################
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


########################################################################################################################
## 发送邮件配置
########################################################################################################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
# 所用邮箱的smtp地址
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 邮箱地址
EMAIL_HOST_USER = 'xxxx'
# 邮箱密码
EMAIL_HOST_PASSWORD = 'xxxx'
# 发件箱名字，和邮箱地址一样就行了
DEFAULT_FROM_EMAIL = 'xxxx'


########################################################################################################################
## 其他配置
########################################################################################################################
# 本地测试
SERVER_URL = '127.0.0.1:8000'


# 分页规则
PAGINATION_SETTINGS = {
    # 中间部分显示的页码数
    'PAGE_RANGE_DISPLAYED': 5,
    # 前后页码数
    'MARGIN_PAGES_DISPLAYED': 2,
    # 是否显示第一页
    'SHOW_FIRST_PAGE_WHEN_INVALID': False,
}


# 远程服务器
# 本地测试
Webssh_ip = '192.168.199.90'

Webssh_port = '9000'

# 维护人员用户名
Product_user = 'demo'

# 系统超级用户
System_superuser = 'admin'


