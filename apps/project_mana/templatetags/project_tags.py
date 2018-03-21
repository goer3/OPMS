########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.db.models import Q
from django import template
from django.db.models import Count


########################################################################################################################
## 系统自带模块导入
########################################################################################################################
import json
import datetime

########################################################################################################################
## 自建模块导入
########################################################################################################################
from project_mana.models import *


register = template.Library()

########################################################################################################################
## 获取分类下文档名称
########################################################################################################################
@register.simple_tag
def get_tag_doc(tid):
    return InstallDoc.objects.filter(doc_tag__id=int(tid))


########################################################################################################################
## 获取文档的标签
########################################################################################################################
@register.simple_tag
def get_doc_tag(doc_id):
    doc = InstallDoc.objects.get(id=int(doc_id))
    tag_list = []
    tags = doc.doc_tag.all()
    if tags.exists():
        for each in tags:
            # print(each.id)
            tag_list.append(each.id)
    return tag_list

