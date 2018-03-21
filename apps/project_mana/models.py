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
## 项目分类
########################################################################################################################
class ProjectCategory(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='分类名')
    dev_group = models.CharField(max_length=64, blank=True, null=True, verbose_name='开发团队Leader')
    desc = models.TextField(blank=True, null=True, verbose_name='项目分类说明')
    is_use = models.BooleanField(default=True, verbose_name='是否启用')
    add_user = models.ForeignKey(UserProfile, verbose_name='添加者')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name_plural = '项目类别'

    def __str__(self):
        return self.name


########################################################################################################################
## 项目
########################################################################################################################
class Project(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='项目名')
    cate = models.ForeignKey(ProjectCategory, verbose_name='所属分类')
    desc = models.TextField(blank=True, null=True, verbose_name='项目说明')
    is_use = models.BooleanField(default=True, verbose_name='是否启用')
    add_user = models.ForeignKey(UserProfile, verbose_name='添加者')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name_plural = '项目'

    def __str__(self):
        return self.name


########################################################################################################################
## 项目详情
########################################################################################################################
class ProjectInfo(models.Model):
    project = models.ForeignKey(Project, verbose_name='项目')
    ask_user = models.CharField(max_length=64, verbose_name='发起者')
    op_user = models.CharField(max_length=64, verbose_name='运维')
    dba_user = models.CharField(max_length=64, verbose_name='DBA')
    app_server = models.CharField(max_length=256, verbose_name='应用服务器')
    app_desc = models.TextField(blank=True, null=True, verbose_name='应用服务器备注')
    data_server = models.CharField(max_length=256, verbose_name='数据库服务器')
    data_desc = models.TextField(blank=True, null=True, verbose_name='数据库服务器备注')
    run_env = models.CharField(max_length=256, verbose_name='运行环境')
    doc = models.TextField(verbose_name='运维部署文档')
    add_user = models.ForeignKey(UserProfile, verbose_name='添加者')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name_plural = '项目详情'

    def __str__(self):
        return "%s - %s" % (self.project, self.ask_user)


########################################################################################################################
## 安装文档标签
########################################################################################################################
class InstallDocTag(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='标签名称')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name_plural = '文档标签'

    def __str__(self):
        return self.name


########################################################################################################################
## 项目详情
########################################################################################################################
class InstallDoc(models.Model):
    doc_title = models.CharField(max_length=128, verbose_name='文章标题')
    doc_content = models.TextField(verbose_name='文章正文')
    doc_tag = models.ManyToManyField(InstallDocTag, blank=True, verbose_name='文档标签')
    doc_author = models.ForeignKey(UserProfile, verbose_name='作者')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name_plural = '安装文档'

    def __str__(self):
        return self.doc_title
























