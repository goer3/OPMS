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
from record.models import Provinces, Cities,Areas


########################################################################################################################
## 服务列表视图
########################################################################################################################
class ServiceListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'deploy_service'
        web_func = 'service'
        content_title = '服务列表'

        services = ProductionService.objects.all()

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            services = services.filter(
                Q(name__icontains=keywords) | \
                Q(add_user__nick_name__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        service_nums = services.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(services, 15, request=request)

        # 分页处理后的 QuerySet
        services = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'service_nums': service_nums,
            'services': services,
        }
        return render(request, 'online_deploy/service_list.html', context=context)


########################################################################################################################
## 添加服务视图
########################################################################################################################
class AddServiceView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            if (request.POST.get('name') is not None) or (request.POST.get('name') != ''):
                service_name = ProductionService.objects.filter(name=request.POST.get('name'))
                if service_name.exists():
                    return HttpResponse('{"status":"fail", "msg":"服务名称已存在，添加失败！"}', content_type='application/json')
                service = ProductionService()
                service.name = request.POST.get('name')
                service.add_user = request.user
                service.save()
                return HttpResponse('{"status":"success", "msg":"服务添加成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"服务添加失败！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"服务添加失败！"}', content_type='application/json')


########################################################################################################################
## 修改服务视图
########################################################################################################################
class ChangeServiceView(LoginRequiredMixin, View):
    def post(self, request, s_id):
        try:
            old_service = ProductionService.objects.get(id=int(s_id))
            if (request.POST.get('name') is not None) or (request.POST.get('name') != ''):
                service_name = ProductionService.objects.exclude(id=int(s_id)).filter(name=request.POST.get('name'))
                if service_name.exists():
                    return HttpResponse('{"status":"fail", "msg":"服务名称已存在，修改失败！"}', content_type='application/json')
                old_service.delete()
                service = ProductionService()
                service.id = old_service.id
                service.name = request.POST.get('name')
                service.add_user = request.user
                service.save()
                return HttpResponse('{"status":"success", "msg":"服务修改成功！"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"服务修改失败！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"服务修改失败！"}', content_type='application/json')


########################################################################################################################
## 中间件列表视图
########################################################################################################################
class MiddlewareRecordListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'deploy_service'
        web_func = 'middleware'
        content_title = '环境版本'

        services = ProductionService.objects.all()

        middlewares = MiddlewareRecord.objects.all().order_by('add_time')

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            middlewares = middlewares.filter(
                Q(service__name__icontains=keywords) | \
                Q(ps__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        middleware_nums = middlewares.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(middlewares, 15, request=request)

        # 分页处理后的 QuerySet
        middlewares = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'services': services,
            'middleware_nums': middleware_nums,
            'middlewares': middlewares,
        }
        return render(request, 'online_deploy/middleware_record_list.html', context=context)


########################################################################################################################
## 添加中间件视图
########################################################################################################################
class AddMiddlewareView(LoginRequiredMixin, View):
    def post(self, request):
        add_middleware_form = AddMiddlewareForm(request.POST)
        if add_middleware_form.is_valid():
            middleware = MiddlewareRecord()
            middleware.pro = Provinces.objects.get(id=int(request.POST.get('pro')))
            if (request.POST.get('city') is not None) and (request.POST.get('city') != ''):
                middleware.city = Cities.objects.get(id=int(request.POST.get('city')))
            if (request.POST.get('area') is not None) and (request.POST.get('area') != ''):
                middleware.area = Areas.objects.get(id=int(request.POST.get('area')))
            middleware.service = ProductionService.objects.get(id=int(request.POST.get('service')))
            middleware.tomcat_version = request.POST.get('tomcat_version')
            middleware.jdk_version = request.POST.get('jdk_version')
            if (request.POST.get('other_version') is not None) and (request.POST.get('other_version') != ''):
                middleware.other_version = request.POST.get('other_version')
            middleware.add_user = request.user
            if (request.POST.get('ps') is not None) and (request.POST.get('ps') != ''):
                middleware.ps = request.POST.get('ps')
            middleware.save()
            return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败！"}', content_type='application/json')


########################################################################################################################
## 修改中间件视图
########################################################################################################################
class ChangeMiddlewareView(LoginRequiredMixin, View):
    def post(self, request, m_id):
        old_record = MiddlewareRecord.objects.get(id=int(m_id))
        change_middleware_form = AddMiddlewareForm(request.POST)
        if change_middleware_form.is_valid():
            old_record.delete()
            middleware = MiddlewareRecord()
            middleware.id = old_record.id
            middleware.pro = Provinces.objects.get(id=int(request.POST.get('pro')))
            if (request.POST.get('city') is not None) and (request.POST.get('city') != ''):
                middleware.city = Cities.objects.get(id=int(request.POST.get('city')))
            if (request.POST.get('area') is not None) and (request.POST.get('area') != ''):
                middleware.area = Areas.objects.get(id=int(request.POST.get('area')))
            middleware.service = ProductionService.objects.get(id=int(request.POST.get('service')))
            middleware.tomcat_version = request.POST.get('tomcat_version')
            middleware.jdk_version = request.POST.get('jdk_version')
            if (request.POST.get('other_version') is not None) and (request.POST.get('other_version') != ''):
                middleware.other_version = request.POST.get('other_version')
            middleware.add_user = request.user
            if (request.POST.get('ps') is not None) and (request.POST.get('ps') != ''):
                middleware.ps = request.POST.get('ps')
            middleware.save()
            return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改失败！"}', content_type='application/json')


########################################################################################################################
## 删除中间件视图
########################################################################################################################
class DeleteMiddlewareView(LoginRequiredMixin, View):
    def post(self, request, m_id):
        try:
            record = MiddlewareRecord.objects.get(id=int(m_id))
            record.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败！"}', content_type='application/json')


########################################################################################################################
## 发布列表视图
########################################################################################################################
class DeployRecordListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'deploy_service'
        web_func = 'deploy'
        content_title = '产品发布'

        services = ProductionService.objects.all()

        deploys = DeployRecord.objects.all().order_by('-deploy_time')

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            deploys = deploys.filter(
                Q(service__name__icontains=keywords) | \
                Q(ps__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        deploy_nums = deploys.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(deploys, 15, request=request)

        # 分页处理后的 QuerySet
        deploys = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'services': services,
            'deploy_nums': deploy_nums,
            'deploys': deploys,
        }
        return render(request, 'online_deploy/deploy_record_list.html', context=context)


########################################################################################################################
## 添加发布记录视图
########################################################################################################################
class AddDeployRecordView(LoginRequiredMixin, View):
    def post(self, request):
        add_deploy_form = AddDeployRecordForm(request.POST)
        if add_deploy_form.is_valid():
            deploys = DeployRecord()
            deploys.pro = Provinces.objects.get(id=int(request.POST.get('pro')))
            if (request.POST.get('city') is not None) and (request.POST.get('city') != ''):
                deploys.city = Cities.objects.get(id=int(request.POST.get('city')))
            if (request.POST.get('area') is not None) and (request.POST.get('area') != ''):
                deploys.area = Areas.objects.get(id=int(request.POST.get('area')))
            deploys.service = ProductionService.objects.get(id=int(request.POST.get('service')))
            if (request.POST.get('tag_address') is not None) and (request.POST.get('tag_address') != ''):
                deploys.tag_address = request.POST.get('tag_address')
            deploys.deploy_time = request.POST.get('deploy_time')
            deploys.add_user = request.user
            if (request.POST.get('ps') is not None) and (request.POST.get('ps') != ''):
                deploys.ps = request.POST.get('ps')
            deploys.save()

            # 发送消息
            create_msg = UserMessage()
            create_msg.send_user = UserProfile.objects.get(username=settings.System_superuser)
            create_msg.send_to = 0
            address = Provinces.objects.get(id=int(request.POST.get('pro'))).name
            if (request.POST.get('city') is not None) and (request.POST.get('city') != ''):
                address = address + Cities.objects.get(id=int(request.POST.get('city'))).name
            if (request.POST.get('area') is not None) and (request.POST.get('area') != ''):
                address = address + Areas.objects.get(id=int(request.POST.get('area'))).name
            create_msg.msg_content = '用户 <b style="color: red;">%s</b> 更新发布了【<b style="color: orangered;">%s</b>】的【<b style="color: blue;">%s</b>】请知悉！' % (request.user.nick_name, address, deploys.service.name )
            create_msg.save()

            return HttpResponse('{"status":"success", "msg":"添加成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败！"}', content_type='application/json')



########################################################################################################################
## 修改发布视图
########################################################################################################################
class ChangeDeployRecordView(LoginRequiredMixin, View):
    def post(self, request, d_id):
        old_record = DeployRecord.objects.get(id=int(d_id))
        add_deploy_form = AddDeployRecordForm(request.POST)
        if add_deploy_form.is_valid():
            old_record.delete()
            deploys = DeployRecord()
            deploys.id = old_record.id
            deploys.pro = Provinces.objects.get(id=int(request.POST.get('pro')))
            if (request.POST.get('city') is not None) and (request.POST.get('city') != ''):
                deploys.city = Cities.objects.get(id=int(request.POST.get('city')))
            if (request.POST.get('area') is not None) and (request.POST.get('area') != ''):
                deploys.area = Areas.objects.get(id=int(request.POST.get('area')))
            deploys.service = ProductionService.objects.get(id=int(request.POST.get('service')))
            if (request.POST.get('tag_address') is not None) and (request.POST.get('tag_address') != ''):
                deploys.tag_address = request.POST.get('tag_address')
            deploys.deploy_time = request.POST.get('deploy_time')
            deploys.add_user = request.user
            if (request.POST.get('ps') is not None) and (request.POST.get('ps') != ''):
                deploys.ps = request.POST.get('ps')
            deploys.save()
            return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改失败！"}', content_type='application/json')


########################################################################################################################
## 删除记录视图
########################################################################################################################
class DeleteDeployRecordView(LoginRequiredMixin, View):
    def post(self, request, d_id):
        try:
            record = DeployRecord.objects.get(id=int(d_id))
            record.delete()
            return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除失败！"}', content_type='application/json')










