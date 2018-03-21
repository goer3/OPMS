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
## 主机列表视图
########################################################################################################################
class HostListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'asset'
        web_func = 'host'
        content_title = '主机列表'
        servers = ServerInfo.objects.all().order_by('-add_time')
        systems = System.objects.all()
        idcs = IDC.objects.all()
        Webssh_ip = settings.Webssh_ip
        Webssh_port = settings.Webssh_port

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            servers = servers.filter(
                Q(ip_addr__icontains=keywords) | \
                Q(server_name__icontains=keywords) | \
                Q(pro_name__icontains=keywords) | \
                Q(idc__name__icontains=keywords) | \
                Q(ask_user__icontains=keywords) | \
                Q(ps__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        server_nums = servers.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(servers, 15, request=request)

        # 分页处理后的 QuerySet
        servers = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'server_nums': server_nums,
            'servers': servers,
            'systems': systems,
            'idcs': idcs,
            'Webssh_ip': Webssh_ip,
            'Webssh_port': Webssh_port,
        }
        return render(request, 'asset/host_list.html', context=context)


########################################################################################################################
## 添加主机视图
########################################################################################################################
class AddHostView(LoginRequiredMixin, View):
    def post(self, request):
        add_host_form = AddHostForm(request.POST)
        if add_host_form.is_valid():
            # 判断记录是否存在
            if ServerInfo.objects.filter(ip_addr=request.POST.get('ip_addr')).filter(idc__id=int(request.POST.get('idc'))):
                return HttpResponse('{"status":"fail", "msg":"记录已存在！"}', content_type='application/json')

            # 如果不存在则添加
            host = ServerInfo()
            host.ip_addr = request.POST.get('ip_addr')
            host.server_name = request.POST.get('server_name')
            system = System.objects.get(id=int(request.POST.get('system')))
            host.system = system
            host.pro_name = request.POST.get('pro_name')
            idc = IDC.objects.get(id=int(request.POST.get('idc')))
            host.idc = idc
            host.disk = int(request.POST.get('disk'))
            host.memory = int(request.POST.get('memory'))
            host.add_user = request.user
            host.ask_user = request.POST.get('ask_user')
            host.user_name = request.POST.get('user_name')
            host.pass_word = request.POST.get('pass_word')
            host.port = request.POST.get('port')
            host.ps = request.POST.get('ps')
            host.save()
            return HttpResponse('{"status":"success", "msg":"记录添加成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"记录添加失败！"}', content_type='application/json')


########################################################################################################################
## 修改主机视图
########################################################################################################################
class ChangeHostView(LoginRequiredMixin, View):
    def post(self, request, h_id):
        change_host_form = ChangeHostForm(request.POST)
        if change_host_form.is_valid():
            # 旧的记录
            old_host = ServerInfo.objects.get(id=int(h_id))
            old_user = old_host.add_user
            old_host.delete()
            # 更新记录
            host = ServerInfo()
            host.id = int(h_id)
            host.ip_addr = request.POST.get('ip_addr')
            host.server_name = request.POST.get('server_name')
            system = System.objects.get(id=int(request.POST.get('system')))
            host.system = system
            host.pro_name = request.POST.get('pro_name')
            idc = IDC.objects.get(id=int(request.POST.get('idc')))
            host.idc = idc
            host.disk = int(request.POST.get('disk'))
            host.memory = int(request.POST.get('memory'))
            host.add_user = old_user
            host.ask_user = request.POST.get('ask_user')
            host.user_name = request.POST.get('user_name')
            host.pass_word = request.POST.get('pass_word')
            host.port = request.POST.get('port')
            host.ps = request.POST.get('ps')
            host.save()
            return HttpResponse('{"status":"success", "msg":"记录修改成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"记录修改失败！"}', content_type='application/json')


########################################################################################################################
## 删除主机视图
########################################################################################################################
class DeleteHostView(LoginRequiredMixin, View):
    def post(self, request, h_id):
        try:
            host = ServerInfo.objects.get(id=int(h_id))
            host.delete()
            return HttpResponse('{"status":"success", "msg":"记录删除成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"记录删除失败！"}', content_type='application/json')


########################################################################################################################
## wessh主机视图
########################################################################################################################
class WebSSHView(LoginRequiredMixin, View):
    def post(self, request, serv_id):
        server = ServerInfo.objects.get(id=int(serv_id))
        ret = {}
        try:
            ip = server.ip_addr
            port = server.port
            username = server.user_name
            password = server.pass_word
            ret = {"ip": ip, 'port': port, "username": username, 'password': password, "static": True}
            # 保存记录
            ssh_history = WebsshHistory()
            ssh_history.user = request.user
            ssh_history.server_ip = ip
            ssh_history.server_user = username
            ssh_history.user_ip = request.META['REMOTE_ADDR']
            ssh_history.save()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '请求错误,{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


########################################################################################################################
## wessh记录列表
########################################################################################################################
class WebSSHListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'asset'
        web_func = 'ssh'
        content_title = '远程记录'
        ssh_logs = WebsshHistory.objects.all().order_by('-add_time')

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            ssh_logs = ssh_logs.filter(
                Q(server_ip__icontains=keywords) | \
                Q(server_user__icontains=keywords) | \
                Q(user__nick_name__icontains=keywords) | \
                Q(user_ip__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        logs_nums = ssh_logs.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(ssh_logs, 15, request=request)

        # 分页处理后的 QuerySet
        ssh_logs = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'logs_nums': logs_nums,
            'ssh_logs': ssh_logs,
        }
        return render(request, 'asset/ssh_history_list.html', context=context)


########################################################################################################################
## 端口映射列表
########################################################################################################################
class PortMapListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'asset'
        web_func = 'port'
        content_title = '端口映射'
        ports = PortMap.objects.all().order_by('-add_time')

        # 记录数量
        port_nums = ports.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(ports, 15, request=request)

        # 分页处理后的 QuerySet
        ports = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'port_nums': port_nums,
            'ports': ports,
        }
        return render(request, 'asset/portmap_list.html', context=context)


########################################################################################################################
## 添加映射视图
########################################################################################################################
class AddPortMapView(LoginRequiredMixin, View):
    def post(self, request):
        add_portmap_form = AddPortMapForm(request.POST)
        if add_portmap_form.is_valid():
            # 判断记录是否存在
            if PortMap.objects.filter(in_ip=request.POST.get('in_ip')).filter(in_port=request.POST.get('in_port')):
                return HttpResponse('{"status":"fail", "msg":"映射已存在！"}', content_type='application/json')

            # 添加新记录
            portmap = PortMap()
            portmap.in_ip = request.POST.get('in_ip')
            portmap.in_port = request.POST.get('in_port')
            portmap.out_ip = request.POST.get('out_ip')
            portmap.out_port = request.POST.get('out_port')
            portmap.ask_user = request.POST.get('ask_user')
            portmap.use_for = request.POST.get('use_for')
            portmap.start_time = request.POST.get('start_time')
            portmap.stop_time = request.POST.get('stop_time')
            portmap.handling_user = request.user
            portmap.ps = request.POST.get('ps')
            portmap.save()

            return HttpResponse('{"status":"success", "msg":"映射记录添加成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"映射记录添加失败！"}', content_type='application/json')


########################################################################################################################
## 删除映射视图
########################################################################################################################
class DeletePortMapView(LoginRequiredMixin, View):
    def post(self, request, p_id):
        try:
            ports = PortMap.objects.get(id=int(p_id))
            ports.delete()
            return HttpResponse('{"status":"success", "msg":"映射记录删除成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"映射记录删除失败！"}', content_type='application/json')


########################################################################################################################
## 修改映射视图
########################################################################################################################
class ChangePortMapView(LoginRequiredMixin, View):
    def post(self, request, p_id):
        change_portmap_form = AddPortMapForm(request.POST)
        if change_portmap_form.is_valid():
            # 删除旧的记录
            old_ports = PortMap.objects.get(id=int(p_id))
            old_user = old_ports.handling_user
            old_ports.delete()
            # 添加新的记录
            portmap = PortMap()
            portmap.in_ip = request.POST.get('in_ip')
            portmap.in_port = request.POST.get('in_port')
            portmap.out_ip = request.POST.get('out_ip')
            portmap.out_port = request.POST.get('out_port')
            portmap.ask_user = request.POST.get('ask_user')
            portmap.use_for = request.POST.get('use_for')
            portmap.start_time = request.POST.get('start_time')
            portmap.stop_time = request.POST.get('stop_time')
            portmap.handling_user = old_user
            portmap.ps = request.POST.get('ps')
            portmap.save()
            return HttpResponse('{"status":"success", "msg":"映射记录修改成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"映射记录修改失败！"}', content_type='application/json')







