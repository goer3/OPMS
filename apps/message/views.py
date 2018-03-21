########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views import View
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.db.models import Q

########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import json
import datetime
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

########################################################################################################################
## 自建模块导入
########################################################################################################################
from .forms import *
from .models import *
from utils.mixin_utils import *
from opms_project import settings


########################################################################################################################
## 用户反馈视图
########################################################################################################################
class UserFeedbackMessageView(LoginRequiredMixin, View):
    def get(self, request):
        web_func = 'feedback'
        context = {
            'web_func': web_func,
        }
        return render(request, 'message/feedback_message.html', context=context)

    def post(self, request):
        feedback_form = UserFeedbackMessageForm(request.POST)
        if feedback_form.is_valid():
            message_obj = UserFeedbackMessage()
            message_obj.user = request.user
            message_obj.message = request.POST.get('message')
            message_obj.save()

            # 发送消息给指定用户
            user_msg = UserMessage()
            user_msg.send_user = request.user
            user_msg.send_to = UserProfile.objects.get(username=settings.Product_user).id
            user_msg.msg_content = request.POST.get('message')
            user_msg.save()

            return HttpResponse('{"status":"success", "msg":"反馈成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"反馈失败！"}', content_type='application/json')


########################################################################################################################
## 用户消息视图
########################################################################################################################
class UserMessageListView(LoginRequiredMixin, View):
    def get(self, request):
        # web_title = 'user_manage'

        web_func = 'message_list'

        superuser = settings.System_superuser

        all_users = UserProfile.objects.all()

        # 加入的天数
        join_days = (datetime.datetime.now() - request.user.date_joined).days

        # 用户消息
        user_msgs = UserMessage.objects.filter(Q(send_to=request.user.id) | Q(send_to=0) | Q(send_user=request.user)).order_by('-update_time')

        # 用户消息选择
        if request.GET.get('msg_status') is not None:
            if request.GET.get('msg_status') != 'all':
                msg_status = request.GET.get('msg_status')
                # 如果查询的是全部未读
                if msg_status == 'notread':
                    user_read = UserReadMessage.objects.filter(user=request.user)
                    read_list = []
                    if user_read.exists():
                        for each in user_read:
                            read_list.append(each.msg_id)
                        user_msgs = user_msgs.exclude(id__in=read_list)
                    user_msgs = user_msgs.exclude(send_user=request.user)
                # 所有用户信息
                elif msg_status == 'user_all':
                    user_msgs = user_msgs.exclude(send_to=0)
                # 所有用户未读信息
                elif msg_status == 'user_notread':
                    user_read = UserReadMessage.objects.filter(user=request.user)
                    read_list = []
                    if user_read.exists():
                        for each in user_read:
                            read_list.append(each.msg.id)
                        user_msgs = user_msgs.exclude(id__in=read_list)
                    user_msgs = user_msgs.exclude(send_to=0).exclude(send_user=request.user)
                # 所有我的消息
                elif msg_status == 'me':
                    user_msgs = user_msgs.filter(send_user=request.user)
                # 其他错误
                else:
                    msg_status = 'all'
            else:
                msg_status = 'all'
        else:
            msg_status = 'all'

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            user_msgs = user_msgs.filter(Q(msg_content__icontains=keywords) | Q(send_user__username__icontains=keywords))

        # 用户数目
        msg_nums = user_msgs.count()
        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(user_msgs, 5, request=request)

        # 分页处理后的 QuerySet
        user_msgs = p.page(page)

        context = {
            # 'web_title': web_title,
            'web_func': web_func,
            'superuser': superuser,
            'join_days': join_days,
            'user_msgs': user_msgs,
            'msg_nums': msg_nums,
            'msg_status': msg_status,
            'all_users': all_users,
        }
        return render(request, 'message/message_list.html', context=context)


########################################################################################################################
## 用户发布通知视图
########################################################################################################################
class UserSendMessageView(LoginRequiredMixin, View):
    def post(self, request):
        msg_content = request.POST.get('UserMessage')
        if msg_content != '' and msg_content is not None:
            msg = UserMessage()
            msg.send_to = request.POST.get('send_to')
            msg.send_user = request.user
            msg.msg_content = request.POST.get('UserMessage')
            msg.save()
            return HttpResponse('{"status":"success", "msg":"发送成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"消息不能为空！"}', content_type='application/json')


########################################################################################################################
## 用户发布评论视图
########################################################################################################################
class UserSendCommentView(LoginRequiredMixin, View):
    def post(self, request):
        msg_comment = request.POST.get('UserComment')
        if msg_comment != '' and msg_comment is not None:
            msg = UserMessage.objects.get(id=request.POST.get('message_id'))
            msg.update_time = datetime.datetime.now()
            msg.save()
            comment = UserComment()
            comment.user_msg = msg
            comment.send_user = request.user
            comment.cmt_content = request.POST.get('UserComment')
            comment.save()
            return HttpResponse('{"status":"success", "msg":"回复成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"消息不能为空！"}', content_type='application/json')


########################################################################################################################
## 删除用户评论视图
########################################################################################################################
class UserDeleteCommentView(LoginRequiredMixin, View):
    def post(self, request):
        comment = UserComment.objects.get(id=request.POST.get('comment_id'))
        if comment != '' and comment is not None:
            comment.user_msg.update_time = datetime.datetime.now()
            comment.user_msg.save()
            comment.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"未知错误！"}', content_type='application/json')


########################################################################################################################
## 标记为已读视图
########################################################################################################################
class ChangeReadStatusView(LoginRequiredMixin, View):
    def post(self, request):
        msg_id = int(request.POST.get('NotReadMessage_id'))
        msg = UserMessage.objects.get(id=msg_id)
        user = request.user
        # 查找记录是否存在
        record = UserReadMessage.objects.filter(user=user, msg__id=msg_id)
        if not record.exists():
            read_msg = UserReadMessage()
            read_msg.user = request.user
            read_msg.msg = msg
            read_msg.is_read = True
            read_msg.save()
        return HttpResponse('{"status":"success", "msg":"标记成功！"}', content_type='application/json')


