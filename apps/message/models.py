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
## 用户反馈
########################################################################################################################
class UserFeedbackMessage(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='反馈用户')
    message = models.TextField(verbose_name='反馈信息')
    add_time = models.DateTimeField(verbose_name='反馈时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户反馈信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


########################################################################################################################
## 用户消息
########################################################################################################################
class UserMessage(models.Model):
    send_user = models.ForeignKey(UserProfile, verbose_name='发送者')
    send_to = models.IntegerField(verbose_name='接收者')
    msg_content = models.TextField(verbose_name='消息')
    add_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.msg_content

    def get_read_user_list(self):
        users = UserReadMessage.objects.filter(msg_id=self.id)
        user_list = []
        for each in users:
            user_list.append(each.user.username)

        return user_list


########################################################################################################################
## 用户评论
########################################################################################################################
class UserComment(models.Model):
    user_msg = models.ForeignKey(UserMessage, verbose_name='用户消息')
    send_user = models.ForeignKey(UserProfile, verbose_name='发送者')
    cmt_content = models.TextField(verbose_name='消息')
    add_time = models.DateTimeField(verbose_name='发送时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.send_user.username


########################################################################################################################
## 用户是否读取消息
########################################################################################################################
class UserReadMessage(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    msg = models.ForeignKey(UserMessage, verbose_name='消息')
    is_read = models.BooleanField(verbose_name='是否读取', default=False)
    add_time = models.DateTimeField(verbose_name='读取时间', auto_now=True)

    class Meta:
        verbose_name = '读取消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username











