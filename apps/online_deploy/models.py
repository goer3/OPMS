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
from record.models import Provinces, Cities, Areas


########################################################################################################################
## 服务表
########################################################################################################################
class ProductionService(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='服务名称')
    add_user = models.ForeignKey(UserProfile, verbose_name='添加人')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '服务表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


########################################################################################################################
## 中间件表
########################################################################################################################
class MiddlewareRecord(models.Model):
    pro = models.ForeignKey(Provinces, verbose_name='省份')
    city = models.ForeignKey(Cities, blank=True, null=True, verbose_name='市级')
    area = models.ForeignKey(Areas, blank=True, null=True, verbose_name='区级')
    service = models.ForeignKey(ProductionService, verbose_name='服务')
    tomcat_version = models.CharField(max_length=20, blank=True, null=True, verbose_name='TOMCAT版本')
    jdk_version = models.CharField(max_length=20, blank=True, null=True, verbose_name='JDK版本')
    other_version = models.TextField(blank=True, null=True, verbose_name='其它服务版本')
    add_user = models.ForeignKey(UserProfile, verbose_name='添加者')
    ps = models.TextField(blank=True, null=True, verbose_name='备注')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '中间件表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.pro.name, self.service)


########################################################################################################################
## 发布记录表
########################################################################################################################
class DeployRecord(models.Model):
    pro = models.ForeignKey(Provinces, verbose_name='省份')
    city = models.ForeignKey(Cities, blank=True, null=True, verbose_name='市级')
    area = models.ForeignKey(Areas, blank=True, null=True, verbose_name='区级')
    service = models.ForeignKey(ProductionService, verbose_name='服务')
    tag_address = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tag')
    deploy_time = models.DateTimeField(verbose_name='发布时间')
    add_user = models.ForeignKey(UserProfile, verbose_name='添加者')
    ps = models.TextField(blank=True, null=True, verbose_name='备注')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '发布记录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.pro.name, self.service)





