########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from users.models import EmailVerificationCode
from django.core.mail import send_mail

########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import random

########################################################################################################################
## 自建模块导入
########################################################################################################################
from opms_project.settings import SERVER_URL, EMAIL_HOST_USER


########################################################################################################################
## 生成随机字符串
########################################################################################################################
def make_ramdom_code(code_length=8):
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
    random_str = ''
    random_length = len(chars) - 1
    for each_str in range(code_length):
        random_str += chars[random.randint(0, random_length)]

    return random_str


########################################################################################################################
## 发送验证码
########################################################################################################################
def send_email_verifycode(email_to, use='register'):
    email_code_record = EmailVerificationCode()

    # 如果是找回密码，那么只需要4个字符的验证码
    if use == 'change_email':
        code = make_ramdom_code(code_length=4)
    else:
        code = make_ramdom_code(code_length=16)

    # 将生成的验证码保存的数据库
    email_code_record.code = code
    email_code_record.email = email_to
    email_code_record.use = use
    email_code_record.save()

    # 注册
    if use == 'register':
        email_title = '[ OPMS ] - 用 户 激 活 ！'
        email_body = '激活链接：{}/active/{}'.format(SERVER_URL, code)
        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email_to,])
        return send_status
    # 忘记密码
    elif use == 'forget':
        email_title = '[ OPMS ] - 用 户 密 码 重 置 ！'
        email_body = '重置密码链接：{}/reset/{}'.format(SERVER_URL, code)
        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email_to, ])
        return send_status
    # 修改认证邮箱
    elif use == 'change_email':
        email_title = '[ OPMS ] - 修 改 用 户 绑 定 邮 箱 ！'
        email_body = '验证码：{}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_HOST_USER, [email_to, ])
        return send_status

