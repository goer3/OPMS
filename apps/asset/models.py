########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.db import models
from django.db.models import Q

########################################################################################################################
## 系统自带模块导入
########################################################################################################################


########################################################################################################################
## 自建模块导入
########################################################################################################################
from users.models import UserProfile


########################################################################################################################
## 操作系统表
########################################################################################################################
class System(models.Model):
    name = models.CharField(max_length=64,  verbose_name='系统名称')
    byte = models.SmallIntegerField(default=64, verbose_name='位数')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        unique_together = ['name', 'byte']
        verbose_name = '操作系统表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.name, self.byte)


########################################################################################################################
## 机房表
########################################################################################################################
class IDC(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='机房名称')
    address = models.CharField(max_length=128, blank=True, null=True, verbose_name='机房地址')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '机房表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


########################################################################################################################
## 服务器详情表
########################################################################################################################
class ServerInfo(models.Model):
    ip_addr = models.GenericIPAddressField(verbose_name='IP地址')
    port = models.SmallIntegerField(default=22, verbose_name='远程端口')
    server_name = models.CharField(max_length=64, verbose_name='主机名')
    system = models.ForeignKey(System, verbose_name='操作系统')
    pro_name = models.CharField(max_length=64, verbose_name='项目名')
    idc = models.ForeignKey(IDC, verbose_name='机房')
    disk = models.SmallIntegerField(default=50, verbose_name='磁盘')
    memory = models.SmallIntegerField(default=8, verbose_name='内存')
    status_choices = ((0, '关机'), (1, '开机'), (2, '其它'))
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='主机状态')
    add_user = models.ForeignKey(UserProfile, verbose_name='添加者')
    ask_user = models.CharField(max_length=64, verbose_name='申请人')
    user_name = models.CharField(max_length=32, verbose_name='登录用户名')
    pass_word = models.CharField(max_length=64, verbose_name='登录密码')
    ps = models.TextField(blank=True, null=True, verbose_name='备注')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '服务器详情表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.ip_addr, self.idc)


########################################################################################################################
## 远程记录表
########################################################################################################################
class WebsshHistory(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    server_ip = models.GenericIPAddressField(verbose_name='服务器IP')
    server_user = models.CharField(max_length=32, verbose_name='登录用户')
    user_ip = models.GenericIPAddressField(verbose_name='用户IP')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '远程记录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.user.nick_name, self.server_ip)


########################################################################################################################
## 端口映射详情表
########################################################################################################################
class PortMap(models.Model):
    out_ip = models.GenericIPAddressField(verbose_name='外网IP')
    out_port = models.SmallIntegerField(verbose_name='外网端口')
    in_ip = models.GenericIPAddressField(verbose_name='内网IP')
    in_port = models.SmallIntegerField(verbose_name='内网端口')
    ask_user = models.CharField(max_length=32, verbose_name='申请人')
    use_for = models.CharField(max_length=128, verbose_name='用途')
    start_time = models.DateField(verbose_name='开始时间')
    stop_time = models.DateField(verbose_name='结束时间')
    handling_user = models.ForeignKey(UserProfile, verbose_name='处理人')
    ps = models.TextField(blank=True, null=True, verbose_name='备注')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '端口映射表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.in_ip, self.in_port)

