# OPMS
结合文档管理，故障管理，服务器资产管理于一体的运维管理平台

项目 DEMO 地址：[http://119.29.105.186:8080/](http://119.29.105.186:8080/)

项目测试账户密码：demo/Test1234


### 项目初始化配置都在 settings.py 中：

【1】数据库配置（MySQL数据库）：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'opms_test',
        'HOST': 'IP地址',
        'PORT': '3306',
        'USER': '用户名',
        'PASSWORD': '密码',
    }
}
```

【2】系统发件箱配置，主要该邮箱要启动 SMTP 功能
```python
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
邮箱地址
EMAIL_HOST_USER = 'xxxx'
邮箱密码
EMAIL_HOST_PASSWORD = 'xxxx'
发件箱名字，和邮箱地址一样就行了
DEFAULT_FROM_EMAIL = 'xxxx'
```


【3】该服务的访问地址配置（服务中会用到，可以是域名）：
```python
SERVER_URL = '127.0.0.1:8000'
```


【4】WEBSSH 服务的本机地址
```python
Webssh_ip = '192.168.199.90'
```


【5】开发者的用户名（便于接收系统消息）
```python
Product_user = 'demo'
```


【6】系统超级用户（系统统一消息发布）
```python
System_superuser = 'admin'
```


### 项目部署使用方法：

【1】MySQL 新建相应的数据库并配置 settings.py 的数据库连接

【2】安装项目所需要的依赖（本项目基于 Python 3.5 开发）
```python
pip install -r require.txt
```

【3】执行数据库同步：
```python
python manage.py migrate
```

【4】创建超级用户：
```python
python manage.py createsuperuser
```

【5】执行 sql 目录下的地区 SQL：依次为 province --> city --> area

【6】启动登录服务访问
