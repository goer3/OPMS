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
from message.models import UserMessage


########################################################################################################################
## 收到任务列表视图
########################################################################################################################
class UnfinishReceiveTaskListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'work_task'
        web_func = 'receive'
        content_title = '待办任务'
        user_list = UserProfile.objects.all()

        tasks = UserWorkTask.objects.filter(send_to=request.user).filter(Q(status=1) | Q(status=2)).order_by('-add_time')

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            tasks = tasks.filter(
                Q(create_user__nick_name__icontains=keywords) | \
                Q(content__icontains=keywords) | \
                Q(ps__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        task_nums = tasks.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(tasks, 15, request=request)

        # 分页处理后的 QuerySet
        tasks = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'task_nums': task_nums,
            'user_list': user_list,
            'tasks': tasks,
        }
        return render(request, 'work_task/receive_task_list.html', context=context)


########################################################################################################################
## 创建任务视图
########################################################################################################################
class AddTaskView(LoginRequiredMixin, View):
    def post(self, request):
        add_task_form = AddTaskForm(request.POST)
        if add_task_form.is_valid():
            # 添加任务
            task = UserWorkTask()
            task.create_user = request.user
            task.send_to = UserProfile.objects.get(id=request.POST.get('send_to'))
            task.content = request.POST.get('content')
            task.task_level = request.POST.get('task_level')
            task.start_time = request.POST.get('start_time')
            task.stop_time = request.POST.get('stop_time')
            task.ps = request.POST.get('ps')
            task.save()

            # 发送消息
            create_msg = UserMessage()
            create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
            create_msg.send_to = task.send_to.id
            create_msg.msg_content = '用户 <b style="color: green;">%s</b> 向你指派了新任务【<b style="color: red;">%s</b>】，请注意跟进！' % (task.create_user.nick_name, task.content)
            create_msg.save()

            return HttpResponse('{"status":"success", "msg":"创建任务成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"创建任务失败！"}', content_type='application/json')


########################################################################################################################
## 终止任务视图
########################################################################################################################
class StopTaskView(LoginRequiredMixin, View):
    def post(self, request, t_id):
        try:
            task = UserWorkTask.objects.get(id=int(t_id))
            task.status = 3
            task.save()

            # 发送消息
            create_msg = UserMessage()
            create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
            create_msg.send_to = task.create_user.id
            create_msg.msg_content = '用户 <b style="color: green;">%s</b> 终止了你指派的任务【<b style="color: red;">%s</b>】，请知悉！' % (request.user.nick_name, task.content)
            create_msg.save()
            return HttpResponse('{"status":"success", "msg":"终止任务成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"终止任务失败！"}', content_type='application/json')


########################################################################################################################
## 完结任务视图
########################################################################################################################
class FinishTaskView(LoginRequiredMixin, View):
    def post(self, request, t_id):
        try:
            task = UserWorkTask.objects.get(id=int(t_id))
            task.status = 0
            task.save()

            # 发送消息
            create_msg = UserMessage()
            create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
            create_msg.send_to = task.create_user.id
            create_msg.msg_content = '用户 <b style="color: green;">%s</b> 完结了你指派的任务【<b style="color: red;">%s</b>】，请知悉！' % (request.user.nick_name, task.content)
            create_msg.save()
            return HttpResponse('{"status":"success", "msg":"完结任务成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"完结任务失败！"}', content_type='application/json')


########################################################################################################################
## 创建任务列表视图
########################################################################################################################
class CreateTaskListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'work_task'
        web_func = 'create'
        content_title = '创建任务'
        user_list = UserProfile.objects.all()

        tasks = UserWorkTask.objects.filter(create_user=request.user).order_by('-add_time')

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            tasks = tasks.filter(
                Q(send_to__nick_name__icontains=keywords) | \
                Q(content__icontains=keywords) | \
                Q(ps__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        task_nums = tasks.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(tasks, 15, request=request)

        # 分页处理后的 QuerySet
        tasks = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'task_nums': task_nums,
            'user_list': user_list,
            'tasks': tasks,
        }
        return render(request, 'work_task/create_task_list.html', context=context)


########################################################################################################################
## 自己终止任务视图
########################################################################################################################
class CreateUserStopTaskView(LoginRequiredMixin, View):
    def post(self, request, t_id):
        try:
            task = UserWorkTask.objects.get(id=int(t_id))
            task.status = 3
            task.save()

            # 发送消息
            create_msg = UserMessage()
            create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
            create_msg.send_to = task.send_to.id
            create_msg.msg_content = '任务发布者 <b style="color: green;">%s</b> 终止了指派给你的任务【<b style="color: red;">%s</b>】，请知悉！' % (request.user.nick_name, task.content)
            create_msg.save()
            return HttpResponse('{"status":"success", "msg":"终止任务成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"终止任务失败！"}', content_type='application/json')


########################################################################################################################
## 自己完结任务视图
########################################################################################################################
class CreateUserFinishTaskView(LoginRequiredMixin, View):
    def post(self, request, t_id):
        try:
            task = UserWorkTask.objects.get(id=int(t_id))
            task.status = 0
            task.save()

            # 发送消息
            create_msg = UserMessage()
            create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
            create_msg.send_to = task.send_to.id
            create_msg.msg_content = '任务发布者 <b style="color: green;">%s</b> 完结了指派给你的任务【<b style="color: red;">%s</b>】，请知悉！' % (request.user.nick_name, task.content)
            create_msg.save()
            return HttpResponse('{"status":"success", "msg":"完结任务成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"完结任务失败！"}', content_type='application/json')


########################################################################################################################
## 修改任务视图
########################################################################################################################
class ChangeTaskView(LoginRequiredMixin, View):
    def post(self, request, t_id):
        old_task = UserWorkTask.objects.get(id=int(t_id))
        add_task_form = AddTaskForm(request.POST)
        if add_task_form.is_valid():
            # 删除旧的记录
            old_task.delete()

            # 添加任务
            task = UserWorkTask()
            task.id = old_task.id
            task.create_user = request.user
            task.send_to = UserProfile.objects.get(id=request.POST.get('send_to'))
            task.content = request.POST.get('content')
            task.task_level = request.POST.get('task_level')
            task.start_time = request.POST.get('start_time')
            task.stop_time = request.POST.get('stop_time')
            task.status = old_task.status
            task.ps = request.POST.get('ps')
            task.save()

            if (old_task.send_to.id) != (UserProfile.objects.get(id=request.POST.get('send_to')).id):
                # 发送给新的指派者消息
                create_msg = UserMessage()
                create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
                create_msg.send_to = task.send_to.id
                create_msg.msg_content = '用户 <b style="color: green;">%s</b> 向你指派了新任务【<b style="color: red;">%s</b>】，请注意跟进！' % (task.create_user.nick_name, task.content)
                create_msg.save()

                # 发送给旧指派者消息
                create_msg = UserMessage()
                create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
                create_msg.send_to = old_task.send_to.id
                create_msg.msg_content = '用户 <b style="color: green;">%s</b> 取消了向你指派的任务【<b style="color: red;">%s</b>】，请知悉！' % (task.create_user.nick_name, old_task.content)
                create_msg.save()
            else:
                # 发送给旧指派者消息
                create_msg = UserMessage()
                create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
                create_msg.send_to = task.send_to.id
                create_msg.msg_content = '用户 <b style="color: green;">%s</b> 修改了向你指派的任务【<b style="color: red;">%s</b>】，请知悉！' % (task.create_user.nick_name, old_task.content)
                create_msg.save()

            return HttpResponse('{"status":"success", "msg":"修改任务成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改任务失败！"}', content_type='application/json')


########################################################################################################################
## 已完结任务列表视图
########################################################################################################################
class FinishTaskListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'work_task'
        web_func = 'finish'
        content_title = '完结任务'
        user_list = UserProfile.objects.all()

        tasks = UserWorkTask.objects.filter(Q(create_user=request.user) | Q(send_to=request.user)).filter(Q(status=0) | Q(status=3)).order_by('-add_time').distinct()

        # 获取用户筛选
        display_chose = request.GET.get('display_chose')

        if (display_chose == '') or (display_chose is None):
            display_chose = 'all'

        if display_chose == 'finish':
            tasks = tasks.filter(status=0)

        if display_chose == 'stop':
            tasks = tasks.filter(status=3)

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            tasks = tasks.filter(
                Q(create_user__nick_name__icontains=keywords) | \
                Q(content__icontains=keywords) | \
                Q(ps__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        task_nums = tasks.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(tasks, 15, request=request)

        # 分页处理后的 QuerySet
        tasks = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'task_nums': task_nums,
            'display_chose': display_chose,
            'user_list': user_list,
            'tasks': tasks,
        }
        return render(request, 'work_task/finish_task_list.html', context=context)


########################################################################################################################
## 激活任务视图
########################################################################################################################
class ActiveTaskView(LoginRequiredMixin, View):
    def post(self, request, t_id):
        try:
            task = UserWorkTask.objects.get(id=int(t_id))
            task.status = 1
            task.save()

            # 发送消息
            create_msg = UserMessage()
            create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
            create_msg.send_to = task.send_to.id
            create_msg.msg_content = '任务发布者 <b style="color: green;">%s</b> 重新激活了指派给你的任务【<b style="color: red;">%s</b>】，请知悉！' % (request.user.nick_name, task.content)
            create_msg.save()
            return HttpResponse('{"status":"success", "msg":"任务激活成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"任务激活失败！"}', content_type='application/json')





