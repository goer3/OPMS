########################################################################################################################
## Django 自带模块导入
########################################################################################################################
from django.db import models
from django.db.models import Q

########################################################################################################################
## 系统自带模块导入
########################################################################################################################


########################################################################################################################
## 自建模块导入
########################################################################################################################
from users.models import UserProfile


########################################################################################################################
## 省市区
########################################################################################################################
class Provinces(models.Model):
    name = models.CharField(max_length=64, verbose_name='省份名')
    province_code = models.CharField(max_length=64, unique=True, verbose_name='省份编码')

    class Meta:
        verbose_name_plural = '省'
        db_table = 'provinces'

    def __str__(self):
        return self.name


class Cities(models.Model):
    city_code = models.CharField(max_length=64, unique=True, verbose_name='市编码')
    name = models.CharField(max_length=64, verbose_name='省份名')
    province = models.ForeignKey(Provinces, verbose_name='所属省份', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('province', 'name')
        verbose_name_plural = '市'
        db_table = 'cities'

    def __str__(self):
        return "%s - %s" % (self.province, self.name)


class Areas(models.Model):
    area_code = models.CharField(max_length=64, unique=True, verbose_name='地区编码')
    name = models.CharField(max_length=64, verbose_name='区名')
    city = models.ForeignKey(Cities, verbose_name='市名', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('city', 'name')
        db_table = 'areas'
        verbose_name_plural = '区'

    def __str__(self):
        return '%s - %s - %s' % (self.city.province, self.city.name, self.name)

########################################################################################################################
## 故障标签
########################################################################################################################
class RecordTags(models.Model):
    name = models.CharField(max_length=64, verbose_name='故障标签名')

    class Meta:
        verbose_name_plural = '故障标签'

    def __str__(self):
        return self.name


########################################################################################################################
## 故障记录
########################################################################################################################
class FaultRecord(models.Model):
    province = models.ForeignKey(Provinces, verbose_name='省份')
    city = models.ForeignKey(Cities, null=True, blank=True, verbose_name='市')
    area = models.ForeignKey(Areas, null=True, blank=True, verbose_name='区')
    platform = models.CharField(max_length=64, verbose_name='平台名称')
    incident = models.CharField(max_length=128, verbose_name='故障事件')
    start_time = models.DateTimeField(verbose_name='故障时间')
    reason = models.TextField(verbose_name='故障原因')
    handling_method = models.TextField(null=True, blank=True, verbose_name='处理办法')
    handling_person = models.ManyToManyField(UserProfile, verbose_name='处理人')
    handling_time = models.DateTimeField(verbose_name='处理时间')
    tag = models.ManyToManyField(RecordTags, blank=True, verbose_name='标签')
    result_choices = ((0, '已处理'), (1, '未处理'), (2, '暂无法处理'))
    result = models.PositiveSmallIntegerField(choices=result_choices, default=0, verbose_name='处理结果')
    ps = models.TextField(blank=True, null=True, verbose_name='备注')
    date = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name_plural = '故障记录'

    def __str__(self):
        return "%s - %s" % (self.province, self.platform)

    def get_hand_user_list(self):
        hand_list = []
        for each in self.handling_person.all():
            hand_list.append(each.id)
        return hand_list

    def get_tag_list(self):
        tag_list = []
        for each in self.tag.all():
            tag_list.append(each.id)
        return tag_list




















