########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


########################################################################################################################
## 系统自带模块导入
########################################################################################################################


########################################################################################################################
## 自建模块导入
########################################################################################################################


########################################################################################################################
## 部门
########################################################################################################################
class UserDepartment(models.Model):
    name = models.CharField(verbose_name='部门名称', max_length=20)
    desc = models.CharField(verbose_name='部门描述', max_length=200, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


########################################################################################################################
## 用户职位
########################################################################################################################
class UserPosition(models.Model):
    name = models.CharField(verbose_name='职位名称', max_length=20)
    desc = models.CharField(verbose_name='职位描述', max_length=200, blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '职位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


########################################################################################################################
## 用户模块
########################################################################################################################
class UserProfile(AbstractUser):
    nick_name = models.CharField(verbose_name='中文名', max_length=10, blank=True, null=True)
    qq = models.CharField(verbose_name='QQ号码', max_length=20, blank=True, null=True)
    wechat = models.CharField(verbose_name='微信号码', max_length=20, blank=True, null=True)
    mobile = models.CharField(verbose_name='手机号码', max_length=20, blank=True, null=True)
    avatar = models.ImageField(verbose_name='用户头像', max_length=200, upload_to='users/avatar/%Y/%m',
                               default='users/avatar/default.png', null=True, blank=True)
    birthday = models.DateField(verbose_name='生日', blank=True, null=True)
    gender = models.CharField(verbose_name='性别', choices=(('male', '男'), ('female', '女')), default='male',
                              max_length=10)
    address = models.CharField(verbose_name='地址', max_length=200, blank=True, null=True)
    department = models.ForeignKey(UserDepartment, verbose_name='部门', blank=True, null=True)
    position = models.ForeignKey(UserPosition, verbose_name='职位', blank=True, null=True)
    desc = models.TextField(verbose_name='其他', blank=True, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_notread_nums(self):
        from message.models import UserMessage, UserReadMessage
        user = UserProfile.objects.filter(id=self.id)
        user_msgs = UserMessage.objects.filter(
            Q(send_to=self.id) | Q(send_to=0) | Q(send_user=user))
        user_read = UserReadMessage.objects.filter(user=user)
        read_list = []
        if user_read.exists():
            for each in user_read:
                read_list.append(each.msg.id)
            user_msgs = user_msgs.exclude(id__in=read_list)
        user_msgs = user_msgs.exclude(send_user=user)
        return user_msgs.count()

    def get_notread_msgs(self):
        from message.models import UserMessage, UserReadMessage
        user = UserProfile.objects.filter(id=self.id)
        user_msgs = UserMessage.objects.filter(
            Q(send_to=self.id) | Q(send_to=0) | Q(send_user=user)).order_by('-update_time')
        user_read = UserReadMessage.objects.filter(user=user)
        read_list = []
        if user_read.exists():
            for each in user_read:
                read_list.append(each.msg.id)
            user_msgs = user_msgs.exclude(id__in=read_list)
        notread_msgs = user_msgs.exclude(send_user=user)
        return notread_msgs


########################################################################################################################
## 邮箱验证码
########################################################################################################################
class EmailVerificationCode(models.Model):
    code = models.CharField(verbose_name='验证码', max_length=20)
    email = models.EmailField(verbose_name='接收邮箱')
    use = models.CharField(verbose_name='用途',
                           choices=(('register', '注册'), ('forget', '忘记密码'), ('change_email', '修改邮箱')), max_length=20)
    is_use = models.BooleanField(verbose_name='是否使用', default=False)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


########################################################################################################################
## 用户登录信息表
########################################################################################################################
class UserLoginRecord(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    agent = models.CharField(verbose_name='客户端', max_length=200, blank=True, null=True)
    city = models.CharField(verbose_name='登录区域', max_length=100, blank=True, null=True)
    ip = models.GenericIPAddressField(verbose_name='客户端IP', blank=True, null=True)
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户登录信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username




















