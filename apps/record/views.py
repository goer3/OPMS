########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
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
import xlwt
from io import StringIO, BytesIO
import time, os, xlwt

########################################################################################################################
## 自建模块导入
########################################################################################################################
from .forms import *
from .models import *
from utils.mixin_utils import *


########################################################################################################################
## 省市区
########################################################################################################################
# 获取省数据
def get_province(request):
    provinceList = Provinces.objects.all()
    list1 = []
    for item in provinceList:
        list1.append([item.id, item.name])
    return JsonResponse({'data': list1})


# 获取市数据
def get_city(request, pid):
    # print(pid)
    cityList = Cities.objects.filter(province=pid)
    list1 = []
    for item in cityList:
        list1.append([item.id, item.name])
    return JsonResponse({'data': list1})


# 获取区县数据
def get_area(request, pid):
    # print(pid)
    AreaList = Areas.objects.filter(city=pid)
    list1 = []
    for item in AreaList:
        list1.append([item.id, item.name])
    return JsonResponse({'data': list1})


########################################################################################################################
## 记录页面
########################################################################################################################
class RecordListView(LoginRequiredMixin, View):
    def get(self, request):
        content_title = '故障列表'
        web_title = 'record'
        web_func = 'record_list'
        user_list = UserProfile.objects.all()
        records = FaultRecord.objects.all().order_by('-start_time')
        tag_list = RecordTags.objects.all()

        export_status = request.GET.get('export', '')

        # 导出所有记录
        if export_status == 'all':
            export_data = records
            if export_data:
                # 创建工作簿
                new_excel = xlwt.Workbook(encoding='utf-8')
                excel_page = new_excel.add_sheet(u'故障记录')

                # 插入第一行标题
                excel_page.write(0, 0, u'省份')
                excel_page.write(0, 1, u'市')
                excel_page.write(0, 2, u'区')
                excel_page.write(0, 3, u'平台名称')
                excel_page.write(0, 4, u'故障事件')
                excel_page.write(0, 5, u'故障时间')
                excel_page.write(0, 6, u'故障原因')
                excel_page.write(0, 7, u'故障标签')
                excel_page.write(0, 8, u'处理办法')
                excel_page.write(0, 9, u'处理人')
                excel_page.write(0, 10, u'处理时间')
                excel_page.write(0, 11, u'处理结果')
                excel_page.write(0, 12, u'备注')
                excel_page.write(0, 13, u'记录添加修改时间')

                # 初始行
                excel_row = 1

                # 插入数据
                for each in export_data:
                    # 获取数据
                    province = each.province.name

                    city = each.city
                    if (city is not None) and (city != ''):
                        city = city.name
                    else:
                        city = '无'

                    area = each.area
                    if (area is not None) and (area != ''):
                        area = each.area.name
                    else:
                        area = '无'

                    platform = each.platform
                    incident = each.incident
                    start_time = each.start_time
                    reason = each.reason

                    tag_obj = each.tag.all()
                    if (tag_obj.exists()):
                        # 拼接标签
                        tag = ''
                        line = [' / '] * len(tag_obj)
                        line[-1] = ''
                        for each_tag, eachline in zip(tag_obj, line):
                            tag = tag + each_tag.name + eachline
                    else:
                        tag = '暂无标签'

                    handling_method = each.handling_method
                    handling_person_obj = each.handling_person.all()

                    # 拼接用户
                    handling_person = ''
                    line = [' / '] * len(handling_person_obj)
                    line[-1] = ''
                    for user, eachline in zip(handling_person_obj, line):
                        handling_person = handling_person + str(user.nick_name) + eachline

                    handling_time = each.handling_time

                    if each.result == 0:
                        result = '已完成'
                    elif each.result == 1:
                        result = '未完成'
                    else:
                        result = '暂时无法完成'

                    ps = each.ps

                    if (ps is None) or (ps == ''):
                        ps = '无'

                    date = each.date

                    time_style = 'YYYY/MM/DD HH:mm'
                    # time_style = 'YYYY/MM/DD hh:mm AM/PM'
                    style = xlwt.XFStyle()
                    style.num_format_str = time_style

                    # 写数据
                    excel_page.write(excel_row, 0, province)
                    excel_page.write(excel_row, 1, city)
                    excel_page.write(excel_row, 2, area)
                    excel_page.write(excel_row, 3, platform)
                    excel_page.write(excel_row, 4, incident)
                    excel_page.write(excel_row, 5, start_time, style)
                    excel_page.write(excel_row, 6, reason)
                    excel_page.write(excel_row, 7, tag)
                    excel_page.write(excel_row, 8, handling_method)
                    excel_page.write(excel_row, 9, handling_person)
                    excel_page.write(excel_row, 10, handling_time, style)
                    excel_page.write(excel_row, 11, result)
                    excel_page.write(excel_row, 12, ps)
                    excel_page.write(excel_row, 13, date, style)

                    # 行数加1
                    excel_row += 1

                time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
                file_name = 'AllRecord_' + time_now + '.xls'

                # 网页下载
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
                output = BytesIO()
                new_excel.save(output)
                output.seek(0)
                response.write(output.getvalue())
                return response

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            records = records.filter(
                Q(province__name__icontains=keywords) | \
                Q(city__name__icontains=keywords) | \
                Q(area__name__icontains=keywords) | \
                Q(platform__icontains=keywords) | \
                Q(incident__icontains=keywords) | \
                Q(reason__icontains=keywords) | \
                Q(handling_method__icontains=keywords) | \
                Q(ps__icontains=keywords)
                )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 搜索条件
        search_province = request.GET.get('province', '')
        search_city = request.GET.get('city', '')
        search_area = request.GET.get('area', '')
        search_start_time = request.GET.get('start_time', '')
        search_stop_time = request.GET.get('stop_time', '')
        search_tag = request.GET.getlist('tag')
        search_user = request.GET.getlist('user')
        search_result = request.GET.get('result', '')

        # 搜索条件筛选
        if (search_province is not None) and (search_province != ''):
            records = records.filter(province__id=int(search_province))
            content_title = '故障搜索结果'

        if (search_city is not None) and (search_city != ''):
            records = records.filter(city__id=int(search_city))
            content_title = '故障搜索结果'

        if (search_area is not None) and (search_area != ''):
            records = records.filter(area__id=int(search_area))
            content_title = '故障搜索结果'

        if (search_start_time is not None) and (search_start_time != ''):
            records = records.filter(start_time__gt=search_start_time)
            content_title = '故障搜索结果'

        if (search_stop_time is not None) and (search_stop_time != ''):
            records = records.filter(start_time__lt=search_stop_time)
            content_title = '故障搜索结果'

        if (len(search_tag) != 0):
            records = records.filter(tag__in=search_tag).distinct()
            content_title = '故障搜索结果'

        if (len(search_user) != 0):
            records = records.filter(handling_person__in=search_user).distinct()
            content_title = '故障搜索结果'

        if (search_result is not None) and (search_result != ''):
            if search_result != 'all':
                records = records.filter(result=int(search_result))
                content_title = '故障搜索结果'

        # 导出搜索记录
        if export_status == 'search':
            export_data = records
            if export_data:
                # 创建工作簿
                new_excel = xlwt.Workbook(encoding='utf-8')
                excel_page = new_excel.add_sheet(u'故障记录')

                # 插入第一行标题
                excel_page.write(0, 0, u'省份')
                excel_page.write(0, 1, u'市')
                excel_page.write(0, 2, u'区')
                excel_page.write(0, 3, u'平台名称')
                excel_page.write(0, 4, u'故障事件')
                excel_page.write(0, 5, u'故障时间')
                excel_page.write(0, 6, u'故障原因')
                excel_page.write(0, 7, u'故障标签')
                excel_page.write(0, 8, u'处理办法')
                excel_page.write(0, 9, u'处理人')
                excel_page.write(0, 10, u'处理时间')
                excel_page.write(0, 11, u'处理结果')
                excel_page.write(0, 12, u'备注')
                excel_page.write(0, 13, u'记录添加修改时间')

                # 初始行
                excel_row = 1

                # 插入数据
                for each in export_data:
                    # 获取数据
                    province = each.province.name

                    city = each.city
                    if (city is not None) and (city != ''):
                        city = city.name
                    else:
                        city = '无'

                    area = each.area
                    if (area is not None) and (area != ''):
                        area = each.area.name
                    else:
                        area = '无'

                    platform = each.platform
                    incident = each.incident
                    start_time = each.start_time
                    reason = each.reason

                    tag_obj = each.tag.all()
                    if (tag_obj.exists()):
                        # 拼接标签
                        tag = ''
                        line = [' / '] * len(tag_obj)
                        line[-1] = ''
                        for each_tag, eachline in zip(tag_obj, line):
                            tag = tag + each_tag.name + eachline
                    else:
                        tag = '暂无标签'

                    handling_method = each.handling_method
                    handling_person_obj = each.handling_person.all()

                    # 拼接用户
                    handling_person = ''
                    line = [' / '] * len(handling_person_obj)
                    line[-1] = ''
                    for user, eachline in zip(handling_person_obj, line):
                        handling_person = handling_person + str(user.nick_name) + eachline

                    handling_time = each.handling_time

                    if each.result == 0:
                        result = '已完成'
                    elif each.result == 1:
                        result = '未完成'
                    else:
                        result = '暂时无法完成'

                    ps = each.ps

                    if (ps is None) or (ps == ''):
                        ps = '无'

                    date = each.date

                    time_style = 'YYYY/MM/DD HH:mm'
                    # time_style = 'YYYY/MM/DD hh:mm AM/PM'
                    style = xlwt.XFStyle()
                    style.num_format_str = time_style

                    # 写数据
                    excel_page.write(excel_row, 0, province)
                    excel_page.write(excel_row, 1, city)
                    excel_page.write(excel_row, 2, area)
                    excel_page.write(excel_row, 3, platform)
                    excel_page.write(excel_row, 4, incident)
                    excel_page.write(excel_row, 5, start_time, style)
                    excel_page.write(excel_row, 6, reason)
                    excel_page.write(excel_row, 7, tag)
                    excel_page.write(excel_row, 8, handling_method)
                    excel_page.write(excel_row, 9, handling_person)
                    excel_page.write(excel_row, 10, handling_time, style)
                    excel_page.write(excel_row, 11, result)
                    excel_page.write(excel_row, 12, ps)
                    excel_page.write(excel_row, 13, date, style)

                    # 行数加1
                    excel_row += 1

                time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
                file_name = 'SearchRecord_' + time_now + '.xls'

                # 网页下载
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
                output = BytesIO()
                new_excel.save(output)
                output.seek(0)
                response.write(output.getvalue())
                return response

        # 记录数量
        record_nums = records.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(records, 10, request=request)

        # 分页处理后的 QuerySet
        records = p.page(page)

        context = {
            'content_title': content_title,
            'web_title': web_title,
            'web_func': web_func,
            'records': records,
            'user_list': user_list,
            'record_nums': record_nums,
            'tag_list': tag_list,

            # 搜索选项
            'search_province': search_province,
            'search_city': search_city,
            'search_area': search_area,
            'search_start_time': search_start_time,
            'search_stop_time': search_stop_time,
            'search_tag': search_tag,
            'search_user': search_user,
            'search_result': search_result,
        }
        return render(request, 'record/record_list.html', context=context)


########################################################################################################################
## 添加记录页面
########################################################################################################################
class AddRecordView(LoginRequiredMixin, View):
    def post(self, request):
        add_record_form = AddRecordForm(request.POST)
        if add_record_form.is_valid():
            add_record_form.save()
            return HttpResponse('{"status":"success", "msg":"记录添加成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"记录添加失败！"}', content_type='application/json')


########################################################################################################################
## 修改记录页面
########################################################################################################################
class ChangeRecordView(LoginRequiredMixin, View):
    def post(self, request):
        change_record_form = AddRecordForm(request.POST)
        change_record = FaultRecord.objects.get(id=request.POST.get('record_id'))

        if change_record_form.is_valid():
            change_record.delete()
            change_record_form.id = request.POST.get('record_id')
            change_record_form.save()
            return HttpResponse('{"status":"success", "msg":"记录修改成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"记录修改失败！"}', content_type='application/json')


########################################################################################################################
## 故障分类页面
########################################################################################################################
class RecordArchiveView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'record'
        web_func = 'record_archive'
        context = {
            'web_title': web_title,
            'web_func': web_func,
        }
        return render(request, 'record/record_archive.html', context=context)


########################################################################################################################
## 归档记录页面
########################################################################################################################
class RecordTimeArchiveView(LoginRequiredMixin, View):
    def get(self, request, year, month):
        web_title = 'record'
        web_func = 'record_archive'
        search_year = year
        search_month = month
        content_title = '<span style="color:orangered">' + str(search_year) + ' 年 ' + str(search_month)  + ' 月</span>归档记录'
        user_list = UserProfile.objects.all()
        tag_list = RecordTags.objects.all()

        records = FaultRecord.objects.filter(start_time__year=search_year, start_time__month=search_month)

        # 记录数量
        record_nums = records.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(records, 10, request=request)

        # 分页处理后的 QuerySet
        records = p.page(page)

        context = {
            'content_title': content_title,
            'web_title': web_title,
            'web_func': web_func,
            'records': records,
            'user_list': user_list,
            'tag_list': tag_list,
            'record_nums': record_nums,
        }
        return render(request, 'record/record_list.html', context=context)


########################################################################################################################
## 标签记录页面
########################################################################################################################
class RecordTagArchiveView(LoginRequiredMixin, View):
    def get(self, request, pid):
        web_title = 'record'
        web_func = 'record_archive'
        search_id = pid
        tag = RecordTags.objects.get(id=search_id)
        content_title = '标签为 <span style="color:orangered">"' + str(tag.name) + '"</span> 的记录 '
        user_list = UserProfile.objects.all()
        tag_list = RecordTags.objects.all()

        records = tag.faultrecord_set.all()

        # 记录数量
        record_nums = records.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(records, 10, request=request)

        # 分页处理后的 QuerySet
        records = p.page(page)

        context = {
            'content_title': content_title,
            'web_title': web_title,
            'web_func': web_func,
            'records': records,
            'user_list': user_list,
            'tag_list': tag_list,
            'record_nums': record_nums,
        }
        return render(request, 'record/record_list.html', context=context)


########################################################################################################################
## 省份记录页面
########################################################################################################################
class RecordProvinceArchiveView(LoginRequiredMixin, View):
    def get(self, request, pid):
        web_title = 'record'
        web_func = 'record_archive'
        search_id = pid
        pro = Provinces.objects.get(id=search_id)
        content_title = '<span style="color:orangered">"' + str(pro.name) + '"</span> 的记录 '
        user_list = UserProfile.objects.all()
        tag_list = RecordTags.objects.all()

        records = pro.faultrecord_set.all()

        # 记录数量
        record_nums = records.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(records, 10, request=request)

        # 分页处理后的 QuerySet
        records = p.page(page)

        context = {
            'content_title': content_title,
            'web_title': web_title,
            'web_func': web_func,
            'records': records,
            'user_list': user_list,
            'tag_list': tag_list,
            'record_nums': record_nums,
        }
        return render(request, 'record/record_list.html', context=context)


########################################################################################################################
## 用户记录页面
########################################################################################################################
class RecordUserArchiveView(LoginRequiredMixin, View):
    def get(self, request, pid):
        web_title = 'record'
        web_func = 'record_archive'
        search_id = pid
        user = UserProfile.objects.get(id=search_id)
        content_title = '<span style="color:orangered">"' + str(user.nick_name) + '"</span> 的记录 '
        user_list = UserProfile.objects.all()
        tag_list = RecordTags.objects.all()

        records = user.faultrecord_set.all()

        # 记录数量
        record_nums = records.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(records, 10, request=request)

        # 分页处理后的 QuerySet
        records = p.page(page)

        context = {
            'content_title': content_title,
            'web_title': web_title,
            'web_func': web_func,
            'records': records,
            'user_list': user_list,
            'tag_list': tag_list,
            'record_nums': record_nums,
        }
        return render(request, 'record/record_list.html', context=context)







