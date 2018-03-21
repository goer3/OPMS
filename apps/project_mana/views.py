########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import json
import datetime
import time
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

########################################################################################################################
## 自建模块导入
########################################################################################################################
from .forms import *
from .models import *
from utils.mixin_utils import *
from opms_project.settings import BASE_DIR


########################################################################################################################
## 分类页面
########################################################################################################################
class ProjectCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        content_title = '项目分类'
        web_title = 'project_mana'
        web_func = 'project_mana'
        project_cates = ProjectCategory.objects.all().order_by('-add_time')

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            project_cates = project_cates.filter(
                Q(name__icontains=keywords) | \
                Q(dev_group__icontains=keywords) | \
                Q(desc__icontains=keywords)
                )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        cate_nums = project_cates.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(project_cates, 2, request=request)

        # 分页处理后的 QuerySet
        project_cates = p.page(page)

        context = {
            'content_title': content_title,
            'web_title': web_title,
            'web_func': web_func,
            'project_cates': project_cates,
            'cate_nums': cate_nums,
        }
        return render(request, 'project_mana/project_category.html', context=context)


########################################################################################################################
## 添加分类
########################################################################################################################
class AddProjectCategoryView(LoginRequiredMixin, View):
    def post(self, request):
        add_cate_form = AddProjectCateForm(request.POST)
        if add_cate_form.is_valid():
            pro_cate = ProjectCategory()
            pro_cate.name = request.POST.get('name')
            pro_cate.dev_group = request.POST.get('dev_group')
            pro_cate.desc = request.POST.get('desc')
            pro_cate.add_user = request.user
            pro_cate.save()
            return HttpResponse('{"status":"success", "msg":"项目类别添加成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"项目类别添加失败！"}', content_type='application/json')


########################################################################################################################
## 管理分类
########################################################################################################################
class ManaProjectCategoryView(LoginRequiredMixin, View):
    def post(self, request):
        cate_id = request.POST.get('cate_id')
        pro_cate = ProjectCategory.objects.get(id=int(cate_id))
        cate_status = request.POST.get('cate_status')
        try:
            if cate_status == 'on':
                pro_cate.is_use = False
                pro_cate.save()
            else:
                pro_cate.is_use = True
                pro_cate.save()
            return HttpResponse('{"status":"success", "msg":"执行成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"执行失败"}', content_type='application/json')


########################################################################################################################
## 项目列表页面
########################################################################################################################
class ProjectListView(LoginRequiredMixin, View):
    def get(self, request, cate_id):
        content_title = '项目列表'
        web_title = 'project_mana'
        web_func = 'project_mana'
        cate_id = int(cate_id)
        cate = ProjectCategory.objects.get(id=cate_id)
        projects = Project.objects.filter(cate=cate_id).order_by('-add_time')

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            projects = projects.filter(
                Q(name__icontains=keywords) | \
                Q(desc__icontains=keywords)
                )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        # 记录数量
        pro_nums = projects.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(projects, 9, request=request)

        # 分页处理后的 QuerySet
        projects = p.page(page)

        context = {
            'content_title': content_title,
            'web_title': web_title,
            'web_func': web_func,
            'cate': cate,
            'projects': projects,
            'pro_nums': pro_nums,
        }
        return render(request, 'project_mana/project_list.html', context=context)


########################################################################################################################
## 添加项目
########################################################################################################################
class AddProjectView(LoginRequiredMixin, View):
    def post(self, request, cate_id):
        add_pro_form = AddProjectForm(request.POST)
        if add_pro_form.is_valid():
            pro = Project()
            pro.name = request.POST.get('name')
            print(cate_id)
            cate = ProjectCategory.objects.get(id=int(cate_id))
            pro.cate = cate
            pro.desc = request.POST.get('desc')
            pro.add_user = request.user
            pro.save()
            return HttpResponse('{"status":"success", "msg":"项目添加成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"项目添加失败！"}', content_type='application/json')


########################################################################################################################
## 管理项目
########################################################################################################################
class ManaProjectView(LoginRequiredMixin, View):
    def post(self, request, cate_id, pro_id):
        pro = Project.objects.get(id=int(pro_id))
        pro_status = request.POST.get('pro_status')
        try:
            if pro_status == 'on':
                pro.is_use = False
                pro.save()
            else:
                pro.is_use = True
                pro.save()
            return HttpResponse('{"status":"success", "msg":"执行成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"执行失败"}', content_type='application/json')


########################################################################################################################
## 项目详情页面
########################################################################################################################
class ProjectDetailView(LoginRequiredMixin, View):
    def get(self, request, cate_id, pro_id):
        content_title = '项目详情'
        web_title = 'project_mana'
        web_func = 'project_mana'
        cate = ProjectCategory.objects.get(id=int(cate_id))
        pro = Project.objects.get(id=int(pro_id))
        try:
            project_infos = ProjectInfo.objects.get(project__id=int(pro_id))
        except Exception as e:
            project_infos = None

        context = {
            'content_title': content_title,
            'web_title': web_title,
            'web_func': web_func,
            'cate': cate,
            'pro': pro,
            'project_infos': project_infos,
        }
        return render(request, 'project_mana/project_detail.html', context=context)


########################################################################################################################
## 添加详情页面
########################################################################################################################
class ProjectInfoView(LoginRequiredMixin, View):
    def post(self, request, cate_id, pro_id):
        pro = Project.objects.get(id=int(pro_id))
        add_proinfo_form =  AddProjectInfoForm(request.POST)
        if add_proinfo_form.is_valid():
            try:
                info = ProjectInfo.objects.get(id=int(request.POST.get('doc_num')))
                info.delete()
                info = ProjectInfo()
                info.project = pro
                info.ask_user = request.POST.get('ask_user')
                info.op_user = request.POST.get('op_user')
                info.dba_user = request.POST.get('dba_user')
                info.app_server = request.POST.get('app_server')
                info.app_desc = request.POST.get('app_desc')
                info.data_server = request.POST.get('data_server')
                info.data_desc = request.POST.get('data_desc')
                info.run_env = request.POST.get('run_env')
                info.doc = request.POST.get('doc')
                info.add_user = request.user
                info.save()
                return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
            except Exception as e:
                info = ProjectInfo()
                info.project = pro
                info.ask_user = request.POST.get('ask_user')
                info.op_user = request.POST.get('op_user')
                info.dba_user = request.POST.get('dba_user')
                info.app_server = request.POST.get('app_server')
                info.app_desc = request.POST.get('app_desc')
                info.data_server = request.POST.get('data_server')
                info.data_desc = request.POST.get('data_desc')
                info.run_env = request.POST.get('run_env')
                info.doc = request.POST.get('doc')
                info.add_user = request.user
                info.save()
                return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改失败！"}', content_type='application/json')


########################################################################################################################
## CKEDITOR 上传图片
########################################################################################################################
@csrf_protect
def upload_image(request):
    if request.method == 'POST':
        callback = request.GET.get('CKEditorFuncNum')
        try:
            # path 修改上传的路径
            path = "upload/ckeditor/image/" + time.strftime("%Y%m%d%H%M%S",time.localtime())
            f = request.FILES["upload"]
            file_name = path + "_" + f.name
            des_origin_f = open(file_name, "wb+")
            # 直接遍历类文件类型就可以生成迭代器了
            for chunk in f:
                des_origin_f.write(chunk)
            des_origin_f.close()
        except Exception as e:
            print(e)
        res = r"<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'/"+file_name+"', '');</script>"
        return HttpResponse(res)
    else:
        raise Http404()


########################################################################################################################
## 安装文档列表
########################################################################################################################
class InstallDocListView(LoginRequiredMixin, View):
    def get(self, request):
        web_title = 'project_mana'
        web_func = 'project_doc'
        content_title = '文档列表'

        tags = InstallDocTag.objects.all()

        docs = InstallDoc.objects.all().order_by('-add_time')

        # 用户搜索
        keywords = request.GET.get('keywords', '')

        if keywords != '':
            docs = docs.filter(
                Q(doc_title__icontains=keywords) | \
                Q(doc_content__icontains=keywords) | \
                Q(doc_tag__name__icontains=keywords)
            )
            content_title = '关键字 <span style="color:orangered">"' + str(keywords) + '"</span> 搜索结果'

        docs = docs.distinct()

        # 记录数量
        doc_nums = docs.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(docs, 9, request=request)

        # 分页处理后的 QuerySet
        docs = p.page(page)

        context = {
            'web_title': web_title,
            'web_func': web_func,
            'content_title': content_title,
            'tags': tags,
            'doc_nums': doc_nums,
            'docs': docs,
        }
        return render(request, 'project_mana/project_doc_list.html', context=context)


########################################################################################################################
## 添加安装文档
########################################################################################################################
class AddInstallDocView(LoginRequiredMixin, View):
    def post(self, request):
        add_ins_doc_form = AddInstallDocForm(request.POST)
        if add_ins_doc_form.is_valid():
            doc = InstallDoc()
            doc.doc_title = request.POST.get('doc_title')
            doc.doc_content = request.POST.get('doc_content')
            doc.doc_author = request.user
            doc.save()

            # 保存 Tag
            tag_list = request.POST.getlist('doc_tag')
            if len(tag_list):
                for each in tag_list:
                    tag = InstallDocTag.objects.get(id=int(each))
                    doc.doc_tag.add(tag)
                    doc.save()

            return HttpResponse('{"status":"success", "msg":"添加文档成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加文档失败！"}', content_type='application/json')


########################################################################################################################
## 管理安装文档
########################################################################################################################
class ManaInstallDocView(LoginRequiredMixin, View):
    def post(self, request):
        doc_id = request.POST.get('doc_id')
        doc = InstallDoc.objects.get(id=int(doc_id))
        try:
            doc.delete()
            return HttpResponse('{"status":"success", "msg":"删除文档成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"fail", "msg":"删除文档失败！"}', content_type='application/json')



########################################################################################################################
## 安装文档详情
########################################################################################################################
class InstallDocDetailView(LoginRequiredMixin, View):
    def get(self, request, doc_id):
        web_title = 'project_mana'
        web_func = 'project_doc'
        tags = InstallDocTag.objects.all()
        doc_info = InstallDoc.objects.get(id=int(doc_id))
        context = {
            'web_title': web_title,
            'web_func': web_func,
            'tags': tags,
            'doc_info': doc_info,
        }
        return render(request, 'project_mana/project_doc_detail.html', context=context)


########################################################################################################################
## 修改安装文档
########################################################################################################################
class ChangeInstallDocView(LoginRequiredMixin, View):
    def post(self, request, doc_id):
        cha_ins_doc_form = AddInstallDocForm(request.POST)
        if cha_ins_doc_form.is_valid():
            old_doc = InstallDoc.objects.get(id=int(doc_id))
            old_doc.delete()
            new_doc = InstallDoc()
            new_doc.id = int(doc_id)
            new_doc.doc_title = request.POST.get('doc_title')
            new_doc.doc_content = request.POST.get('doc_content')
            new_doc.doc_author = request.user
            new_doc.save()

            # 保存 Tag
            tag_list = request.POST.getlist('doc_tag')
            if len(tag_list):
                for each in tag_list:
                    tag = InstallDocTag.objects.get(id=int(each))
                    new_doc.doc_tag.add(tag)
                    new_doc.save()

            return HttpResponse('{"status":"success", "msg":"修改文档成功！"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改文档失败！"}', content_type='application/json')
















