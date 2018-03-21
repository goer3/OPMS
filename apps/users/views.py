########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import json
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
import datetime

########################################################################################################################
## 自建模块导入
########################################################################################################################
from .forms import *
from .models import *
from utils.mixin_utils import *
from utils.sendmail_utils import *
from utils.other_func import *
from project_mana.models import InstallDoc
from record.models import FaultRecord
from message.models import UserMessage


########################################################################################################################
## 首页类视图
########################################################################################################################
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        web_func = 'index'
        # 用户数
        user_nums = UserProfile.objects.all().count()
        # 文档数
        doc_nums = InstallDoc.objects.all().count()
        # 记录数
        record_nums = FaultRecord.objects.all().count()
        # 消息数
        message_nums = UserMessage.objects.filter(
            Q(send_to=request.user.id) | \
            Q(send_to=0)
            ).count()

        # 最近 12 个月
        n = 0
        year_list = []
        month_list = []
        year_now = datetime.datetime.now().year
        month_now = datetime.datetime.now().month
        new_year = year_now
        new_month = month_now

        while n < 12:
            n += 1
            year_list.append(new_year)
            month_list.append(new_month)
            if (month_now - n) > 0:
                new_month = (month_now - n)

            if (month_now - n) == 0:
                new_year = (year_now - 1)
                new_month = 12

            if (month_now - n) < 0:
                new_month = (12 + (month_now - n))

        year_list = list(reversed(year_list))
        month_list = list(reversed(month_list))

        ziped = zip(year_list, month_list)
        nums_list = []
        y_m_list = []

        for each in ziped:
            re_nums = FaultRecord.objects.filter(start_time__year=each[0], start_time__month=each[1]).count()
            nums_list.append(re_nums)
            y_m_list.append(str(each[0]) + '年' + str(each[1]) + '月')

        context = {
            'web_func': web_func,
            'user_nums': user_nums,
            'doc_nums': doc_nums,
            'record_nums': record_nums,
            'message_nums': message_nums,
            'nums_list': nums_list,
            'y_m_list': y_m_list,
        }
        return render(request, 'users/index.html', context=context)


########################################################################################################################
## 用户邮箱登陆
########################################################################################################################
class OtherLoginBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 增加 Email, 同理增加手机都行
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


########################################################################################################################
## 用户登录类视图
########################################################################################################################
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, 'users/login.html', context=context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username')
            pass_word = request.POST.get('password')
            # 系统模块认认证用户
            user = authenticate(username=user_name, password=pass_word)
            # 判断用户认证结果
            if user is not None:
                if user.is_active:
                    login(request, user)
                    login_record = UserLoginRecord()
                    login_record.user = user
                    login_record.agent = request.META['HTTP_USER_AGENT']
                    login_record.ip = request.META['REMOTE_ADDR']
                    login_record.city = get_ip_location(request.META['REMOTE_ADDR'])
                    login_record.save()
                    return HttpResponseRedirect(reverse('users:index'))
                else:
                    msg = '用户未激活！'
                    context = {
                        'msg': msg,
                        'login_form': login_form,
                    }
                    return render(request, 'users/login.html', context=context)
            else:
                msg = '用户名或密码错误！'
                context = {
                    'msg': msg,
                    'login_form': login_form,
                }
                return render(request, 'users/login.html', context=context)
        else:
            context = {
                'login_form': login_form,
            }
            return render(request, 'users/login.html', context=context)


########################################################################################################################
## 用户注销登录视图
########################################################################################################################
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))


########################################################################################################################
## 用户找回密码
########################################################################################################################
class ForgetPasswordView(View):
    def get(self, request):
        return render(request, 'users/forget_password.html', context={})

    def post(self, request):
        # 实例化 email 表单
        forget_password_form = ForgetPasswordForm(request.POST)

        # 判断提交的数据合法性
        if forget_password_form.is_valid():
            email = request.POST.get('email')
            # 查找是否有该邮箱
            if UserProfile.objects.filter(email=email):
                send_status = send_email_verifycode(email, 'forget')
                if send_status:
                    return HttpResponse('{"status":"success", "msg":"发送成功！"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail", "msg":"邮件发送失败！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"发送失败，该用户不存在！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"发送失败，邮箱格式不合法！"}', content_type='application/json')


########################################################################################################################
## 用户重置密码页面
########################################################################################################################
class ResetPasswordView(View):
    def get(self, request, reset_code):
        code = reset_code
        email_records = EmailVerificationCode.objects.filter(code=code, use='forget')
        if email_records:
            email = email_records[0].email
            # 取出该用户最新的忘记密码验证码
            email_record = EmailVerificationCode.objects.filter(email=email, use='forget').order_by('-add_time')[0]

            if email_record.code == code and email_record.is_use == False:
                context = {
                    'email': email,
                }
                return render(request, 'users/reset_password.html', context=context)
            else:
                return HttpResponse('<h2>重置验证码已过期！</h2>')
        else:
            return HttpResponse('<h2>该验证码不存在！</h2>')


########################################################################################################################
## 用户重置密码过程
########################################################################################################################
class ModifyPasswordView(View):
    def post(self, request):
        reset_password_form = ResetPasswordForm(request.POST)
        email = request.POST.get('email')
        if reset_password_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 == pwd2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd1)
                user.save()
                email_record = EmailVerificationCode.objects.filter(use='forget', email=email).order_by('-add_time')[0]
                email_record.is_use = True
                email_record.save()
                return HttpResponse('{"status":"success", "msg":"密码重置成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"密码不一致或不符合长度要求！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"密码不一致或不符合长度要求！"}', content_type='application/json')


########################################################################################################################
## 用户个人信息中心
########################################################################################################################
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'user_manage'
        web_func = 'userinfo'
        change_info_status = ''
        context = {
            'web_title': web_title,
            'web_func': web_func,
            'change_info_status': json.dumps(change_info_status),
        }
        return render(request, 'users/user_info.html', context=context)

    def post(self, request):
        web_title = 'user_manage'
        web_func = 'userinfo'
        change_userinfo_form = ChangeUserInfoForm(request.POST)
        if change_userinfo_form.is_valid():
            user = request.user
            user.address = request.POST.get('address')
            if '年' not in request.POST.get('birthday'):
                user.birthday = request.POST.get('birthday')
            user.gender = request.POST.get('gender')
            user.mobile = request.POST.get('mobile')
            user.qq = request.POST.get('qq')
            user.wechat = request.POST.get('wechat')
            user.desc = request.POST.get('desc')
            user.save()

            change_info_status = 'success'
            context = {
                'web_title': web_title,
                'web_func': web_func,
                'change_info_status': json.dumps(change_info_status),
            }
            return render(request, 'users/user_info.html', context=context)
        else:
            change_info_status = 'fail'
            context = {
                'web_title': web_title,
                'web_func': web_func,
                'change_userinfo_form': change_userinfo_form,
                'change_info_status': json.dumps(change_info_status),
            }
            return render(request, 'users/user_info.html', context=context)


########################################################################################################################
## 上传头像
########################################################################################################################
class ChangeAvatarView(LoginRequiredMixin, View):
    def post(self, request):
        change_avatar_form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user)
        if change_avatar_form.is_valid():
            request.user.save()
            return HttpResponseRedirect(reverse('users:user_info'))
        else:
            return HttpResponseRedirect(reverse('users:user_info'))


########################################################################################################################
## 用户修改密码
########################################################################################################################
class ChangePasswordView(LoginRequiredMixin, View):
    def post(self, request):
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 == pwd2:
                request.user.password = make_password(pwd1)
                request.user.save()
                return HttpResponse('{"status":"success", "msg":"密码修改成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"密码不一致或不符合要求！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"密码不一致或不符合要求！"}', content_type='application/json')


########################################################################################################################
## 发送修改邮箱验证码
########################################################################################################################
class SendChangeEmailCodeView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"fail", "msg":"邮箱已经绑定！"}', content_type='application/json')
        else:
            # 发送验证码
            send_status = send_email_verifycode(email, 'change_email')

            if send_status:
                return HttpResponse('{"status":"success", "msg":"邮件发送成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"邮件发送失败！"}', content_type='application/json')


########################################################################################################################
## 用户修改绑定邮箱
########################################################################################################################
class ChangeEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        email_info = EmailVerificationCode.objects.filter(email=email, code=code, use='change_email', is_use=False)

        if not email_info:
            return HttpResponse('{"status":"fail", "msg":"验证码出错！"}', content_type='application/json')

        # 最新的验证码
        email_record = email_info.order_by('-add_time')[:1][0]
        email_code = email_record.code

        if code == email_code:
            request.user.email = email
            request.user.save()
            email_record.is_use = True
            email_record.save()
            return HttpResponse('{"status":"success", "msg": "修改成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg": "验证码错误！"}', content_type='application/json')


########################################################################################################################
## 其他用户资料
########################################################################################################################
class OtherUserInfoView(LoginRequiredMixin, View):
    def get(self, request, uid):
        web_title = 'user_manage'
        web_func = 'userinfo'
        user_info_list = UserProfile.objects.get(id=uid)
        context = {
            'web_title': web_title,
            'web_func': web_func,
            'user_info_list': user_info_list,
        }
        return render(request, 'users/other_user_info.html', context=context)


########################################################################################################################
## 用户登录记录
########################################################################################################################
class UserLoginRecordView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'user_manage'
        web_func = 'login_record'
        all_records = UserLoginRecord.objects.filter(user=request.user).order_by('-add_time')

        keywords = request.GET.get('keywords', '')

        if keywords != '':
            all_records = all_records.filter(Q(agent__icontains=keywords) | Q(city__icontains=keywords))

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(all_records, 15, request=request)

        # 分页处理后的 QuerySet
        all_records = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'all_records': all_records,
        }
        return render(request, 'users/login_record.html', context=context)


########################################################################################################################
## 用户列表
########################################################################################################################
class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'user_manage'
        web_func = 'user_list'
        all_users = UserProfile.objects.all()
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            all_users = all_users.filter(
                Q(username__icontains=keywords) | Q(nick_name__icontains=keywords) | Q(email__icontains=keywords) | Q(
                    mobile__icontains=keywords) | Q(qq__icontains=keywords) | Q(wechat__icontains=keywords) | Q(
                    desc__icontains=keywords) | Q(department__name__icontains=keywords) | Q(position__name__icontains=keywords))

        if request.GET.get('display_chose') is not None:
            if request.GET.get('display_chose') != 'all':
                display_chose = request.GET.get('display_chose')
                all_users = all_users.filter(gender=display_chose)
            else:
                display_chose = 'all'
        else:
            display_chose = 'all'

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(all_users, 9, request=request)

        # 分页处理后的 QuerySet
        all_users = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'all_users': all_users,
            'display_chose': display_chose,
        }
        return render(request, 'users/user_list.html', context=context)


########################################################################################################################
## 用户状态管理
########################################################################################################################
class UserStatusManaView(LoginRequiredMixin, View):
    def post(self, request, uid):
        if request.user.is_superuser:
            user = UserProfile.objects.get(id=int(uid))
            user_status = request.POST.get('user_status')
            try:
                if user_status == 'on':
                    user.is_active = False
                    user.save()
                else:
                    user.is_active = True
                    user.save()
                return HttpResponse('{"status":"success", "msg":"执行成功！"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"fail", "msg":"执行失败"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"你无权操作"}', content_type='application/json')






















