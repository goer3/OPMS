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
## 任务表
########################################################################################################################
class UserWorkTask(models.Model):
    create_user = models.ForeignKey(UserProfile, related_name='c_user', verbose_name='发起者')
    send_to = models.ForeignKey(UserProfile, related_name='s_user', verbose_name='指派者')
    level_choices = ((1, '紧急'), (2, '一般'), (3, '不急'))
    task_level = models.PositiveSmallIntegerField(choices=level_choices, default=2, verbose_name='紧急程度')
    content = models.TextField(verbose_name='任务内容')
    start_time = models.DateTimeField(verbose_name='开始时间')
    stop_time = models.DateTimeField(verbose_name='截止时间')
    status_choices = ((0, '已完成'), (1, '进行中'), (2, '延期中 '), (3, '已终止'))
    status = models.PositiveSmallIntegerField(choices=status_choices, default=1, verbose_name='任务状态')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    ps = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '任务表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.create_user.nick_name, self.content)






























