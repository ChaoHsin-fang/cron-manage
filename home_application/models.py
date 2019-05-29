# -*- coding: utf-8 -*-
from django.db import models


#  定时任务信息表
class CrontabInfo(models.Model):
    server_ip = models.CharField(u"服务器IP", max_length=100)
    bk_biz_id = models.CharField(u"业务ID", max_length=30)
    bk_biz_name = models.CharField(u"业务名称", max_length=100)
    cron_min = models.CharField(u"分钟", max_length=100)
    cron_hour = models.CharField(u"小时", max_length=100)
    cron_day = models.CharField(u"几号", max_length=100)
    cron_month = models.CharField(u"月", max_length=100)
    cron_week = models.CharField(u"周", max_length=100)
    cron_task = models.CharField(u"定时任务：脚本名称或命令", max_length=3000)
    creator = models.CharField(u"用户", max_length=30)
    status = models.CharField(u"任务状态 0停止 1 启动", max_length=300,default =0)
    create_time = models.DateTimeField(u"创建时间", auto_now=True)
    deleted = models.CharField(u"是否删除 0 未删除 1 删除", max_length =10, default = 0)

    class Meta:
        db_table = 'crontab_info'  # 指明数据库表名


# 任务历史修改记录表
class CrontabChangeHistory(models.Model):
    operator = models.CharField(u"变更操作人:平台当前登录用户", max_length=100)
    cron_task_before = models.CharField(u"变更之前的定时任务", max_length=3000)
    cron_task_after = models.CharField(u"变更之后的定时任务", max_length=3000)
    operation = models.CharField(u"操作 0:无编辑记录,1 :删除 2: 编辑", max_length=100)
    last_edit_time = models.DateTimeField(u"最后编辑时间", auto_now=True)
    cron_info = models.ForeignKey('CrontabInfo',on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.operator+" "+self.cron_task_before+" "+self.cron_task_after+self.operation+" "+self.last_edit_time

    class Meta:
        db_table = 'crontab_change_history'  # 指明数据库表名


# 业务信息表
class BusinessInfo(models.Model):
    bk_biz_id = models.CharField(u"业务id", max_length=100)
    bk_biz_name = models.CharField(u"业务名称", max_length=100)
    current_biz = models.CharField(u"当前业务 标识为1", max_length=100, default= 0)

    class Meta:
        db_table = 'business_info'  # 业务信息表
