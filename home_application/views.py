# -*- coding: utf-8 -*-
import time,HTMLParser
from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request
from django.http import HttpResponse
from home_application.models import CrontabInfo, BusinessInfo, CrontabChangeHistory
from common.log import logger
import traceback,base64
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from blueking.component.shortcuts import get_client_by_user


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def cron_history(request):
    """
    任务历史变更记录
    """
    return render_mako_context(request, '/home_application/cron_history.html')


# 获取服务器IP列表
@csrf_exempt
# @login_exempt
def get_server_list(request):
    if request.method == 'POST':
        bk_host_innerip = search_bk_host(request)
        return render_json(bk_host_innerip)


# 业务信息展示
@csrf_exempt
# @login_exempt
def get_biz(request):
    if request.method == 'POST':
        user = "admin"
        client = get_client_by_user(user)
        kwargs = {"fields": ["bk_biz_id", "bk_biz_name"], }
        result = client.cc.search_business(kwargs)
        biz_info = (result['data'].get('info'))
        # print biz_info
        # 默认显示的第一个业务入库保存
        current_biz = biz_info[0]
        biz_dict ={
            'bk_biz_id':current_biz.get("bk_biz_id"),
            "bk_biz_name":current_biz.get("bk_biz_name"),
            "current_biz" :1,
              }

        if not BusinessInfo.objects.filter(current_biz=1):
            BusinessInfo.objects.create(**biz_dict)
        return render_json(biz_info)


@csrf_exempt
# @login_exempt
# 获取当前业务
def get_current_biz(request):
    if request.method == 'POST':
        bk_biz_id = request.POST.get("bk_biz_id")
        bk_biz_name = request.POST.get("bk_biz_name")
        # print "bk_biz_id%s" % bk_biz_id
        # print "bk_biz_name%s" % bk_biz_name
        # 用户切换的业务覆盖旧业务
        BusinessInfo.objects.filter(current_biz=1).update(bk_biz_id=bk_biz_id,bk_biz_name=bk_biz_name)
        obj = BusinessInfo.objects.get(current_biz=1)
        current_biz_name = obj.bk_biz_name
        # print current_biz_name
        return render_json(current_biz_name)


#  导入入库-服务器列表
def select_server(request):
    # client = get_client_by_request(request)
    # result = client.cc.search_host()
    user = "admin"
    client = get_client_by_user(user)
    obj = BusinessInfo.objects.get(current_biz=1)
    bk_biz_id = obj.bk_biz_id
    param = {"bk_biz_id": bk_biz_id}
    result = client.cc.search_host(param)
    info = result["data"].get("info")
    server_list = []
    for i in info:
        server_list.append(
            {
             "bk_host_innerip": i["host"].get("bk_host_innerip"),
             "bk_host_name" : i["host"].get("bk_host_name"),
             "bk_os_name": i["host"].get("bk_os_name")}
            )
    # print server_list
    return render_json(server_list)


# 服务器定时任务入库
@csrf_exempt
# @login_exempt
def get_server_crontab(request):
    resp = {"result": True,"code": 0,"message": "success",}
    if request.method == 'POST':
        # bk_biz_id = request.POST.get("bk_biz_id")
        obj = BusinessInfo.objects.get(current_biz=1)
        bk_biz_id = obj.bk_biz_id
        ip_list = (request.POST.get("ip")).split(",")
        script_content = "Y2QgL3Zhci9zcG9vbC9jcm9uCmxzCmZvciBpIGluIGBsc2AKZG8KICAgZWNobyAiY3Jvbl91c2VyIjokaQplY2hvICJzdGFydCIKY2F0ICRpCmVjaG8gImVuZCIKZG9uZQ=="
        if ip_list:
            for ip in ip_list:
                kwargs = {
                    "bk_biz_id": bk_biz_id,
                    "script_content": script_content,
                    "script_type": 1,
                    "account": "root",
                    "ip_list": [
                        {"bk_cloud_id": 0, "ip": ip}, ], }
                log_content = execute_script(request,kwargs)
                html_parser = HTMLParser.HTMLParser()
                # for log_content in log_contents:
                # # &gt转义
                crons = html_parser.unescape(log_content)
                cron_time_list = ['cron_min', 'cron_hour', 'cron_day', 'cron_month', 'cron_week']
                cron_list = []
                for item in crons.split("\n"):
                    # print item
                    if not item or '#' == item.lstrip()[0]:
                        continue
                    if item.startswith("cron_user"):
                        user = item[10:]
                        continue
                    elif item == "start":
                        continue
                    cron_time_dict = dict(zip(cron_time_list, item.split(' ')[0:5]))
                    cron_task = ' '
                    for i in item.split(' ')[5:]:
                        cron_task = cron_task + i + ' '
                        cron_time_dict['cron_task'] = cron_task
                        cron_list.append(cron_time_dict)
                    if len(cron_time_dict) <= 3:
                        pass
                    else:
                        cron_time_dict['user'] = user
                    # print "ip%s" % ip
                for c in cron_list:
                    # print "ip%s" % ip
                    dic = {
                     'server_ip':ip,
                     "bk_biz_id":bk_biz_id,
                     "bk_biz_name":obj.bk_biz_name,
                     'cron_min' : c["cron_min"],
                     'cron_hour': c["cron_hour"],
                     'cron_day': c["cron_day"],
                     'cron_month':  c["cron_month"],
                     'cron_week': c["cron_week"],
                     'cron_task':  c["cron_task"],
                     "creator": c["user"],
                     "status":0,
                     "deleted":0,
                           }
                    CrontabInfo.objects.create(**dic)
        return HttpResponse(resp)


# 展示服务器的用户
@csrf_exempt
# @login_exempt
def get_crontab_users(request):
    if request.method == 'POST':
        resp ={'result': True, 'message': u"start a crontab successfully"}
        script_content = "Y2QgL3Zhci9zcG9vbC9jcm9uCmxzCg=="
        obj = BusinessInfo.objects.get(current_biz=1)
        bk_biz_id = obj.bk_biz_id
        ip = request.POST.get("ip")
        # print "bk_biz_id%s" % bk_biz_id
        # print "ip%s" % ip
        if ip:
            kwargs = {
                "bk_biz_id": bk_biz_id,
                "script_content": script_content,
                "script_type": 1,
                "account": "root",
                "ip_list": [
                    {"bk_cloud_id": 0, "ip": ip}, ], }
            result = execute_script(request, kwargs)
            user_list = result.split("\n")
            del user_list[-1]
            return render_json(user_list)
        else:
            return HttpResponse(resp)


# 去掉时间空格
def replace_nbsp(a):
    c = a.replace("&nbsp;", " ")
    return c


# 字符串转换时间对象
def str_to_date(string):
    return datetime.strptime(string,"%Y-%m-%d %H:%M:%S")


# 多条件查询定时任务
@csrf_exempt
# @login_exempt
def search_crontabs(request):
    if request.method == 'POST':
        # 服务器
        server_ip = request.POST.get('ip',None)
        # print "server_ip%s" % server_ip
        # 用户
        creator = request.POST.get('user',None)
        # print "creator%s" % creator
        # print "status%s" % status
        # print "bk_biz_name%s" % bk_biz_name
        # 开始时间
        start_date = request.POST.get('start_date',)
        # 结束时间
        end_date = request.POST.get('end_date',)
        query_set = CrontabInfo.objects.all()
        if start_date < end_date:
            start = replace_nbsp(start_date)
            start_date = str_to_date(start)
            # print "start_date%s" % start_date
            # print type(start_date)
            end = replace_nbsp(end_date)
            end_date = str_to_date(end)
            # print type(end_date)
            # print "end_date%s" % end_date
            query_set = query_set.filter(Q(create_time__gt=start_date, create_time__lte=end_date) & Q(deleted=0))
            # print query_set
        if server_ip:
            query_set = query_set.filter(Q(server_ip=server_ip) & Q(deleted=0))
        if creator:
            query_set = query_set.filter(Q(creator=creator) & Q(deleted=0))
        search_result = []
        for obj in query_set:
            search_result.append(
                {"id": obj.id,
                 "cron_task": obj.cron_task,
                 "cron_expression": obj.cron_min + " " + obj.cron_hour + " " + obj.cron_day + " " + obj.cron_month + " " + obj.cron_week + " ",
                 "creator": obj.creator,
                 "create_time": "%s" % obj.create_time,
                 "server_ip": obj.server_ip,
                 "status": obj.status,
                 "bk_biz_name": obj.bk_biz_name,
                 }
            )
        # print "search_result%s" % search_result
        return render_json(search_result)


# 新建定时任务:本地入库
@csrf_exempt
def create_crontab(request):
    if request.method == 'POST':
        server_ip = request.POST.get('server_ip',None)
        obj = BusinessInfo.objects.get(current_biz=1)
        bk_biz_id = obj.bk_biz_id
        bk_biz_name = obj.bk_biz_name
        cron_min = request.POST.get('cron_min',None)
        cron_hour = request.POST.get('cron_hour',None)
        cron_day = request.POST.get('cron_day',None)
        cron_month = request.POST.get('cron_month',None)
        cron_week = request.POST.get('cron_week',None)
        cron_task = request.POST.get('cron_task',None)
        creator = request.POST.get('creator',None)
        try:
            dic = {
                "server_ip":server_ip,
                "bk_biz_id":bk_biz_id,
                "bk_biz_name":bk_biz_name,
                "cron_min":cron_min,
                "cron_hour":cron_hour,
                "cron_day":cron_day,
                "cron_month":cron_month,
                "cron_week":cron_week,
                "cron_task":cron_task,
                "creator": creator,
                "status":0,
                "deleted":0,
            }
            CrontabInfo.objects.create(**dic)
            time.sleep(2)
            update_to_server(request,bk_biz_id)
            result = {'result': True, 'message': u"新增任务成功"}
        except Exception as e:
            logger.error(u"新增任务失败，%s" % e)
            result = {'result': False, 'message': u"新增任务失败，%s" % e}
        return render_json(result)


# 新增定时任务同步到服务器
def update_to_server(request,bk_biz_id):
    # 获取最新的任务ID
    latest_id = (CrontabInfo.objects.latest("id")).id
    query_set = CrontabInfo.objects.get(id=latest_id)
    for obj in query_set:
        ip = obj.server_ip
        user = obj.creator
        cron = obj.cron_min + " " + obj.cron_hour + " " + obj.cron_day + " " + obj.cron_month + " " + obj.cron_week + " " + obj.cron_task
    crontab = "echo" + " " + "'{cron}'" + ">> /var/spool/cron/{user}" + "\n"
    script = crontab.format(cron=cron, user=user)
    # print script
    script_content = base64_encode(script)
    kwargs = {
        "bk_biz_id": bk_biz_id,
        "script_content": script_content,
        "script_type": 1,
        "account": "root",
        "ip_list": [
            {"bk_cloud_id": 0, "ip": ip}, ], }
    execute_script(request, kwargs)
    return render_json("update new cron to server")


# 编辑:弹出框定时任务展示
@csrf_exempt
def edit_crontab(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        if task_id:
            # task_id = 13
            # print "task_id%s" % task_id
            obj = CrontabInfo.objects.get(id=task_id)
            result_dict = {
                "cron_min": obj.cron_min,
                "cron_hour": obj.cron_hour,
                "cron_day": obj.cron_day,
                "cron_month": obj.cron_month,
                "cron_week": obj.cron_week,
                "cron_task": obj.cron_task,
               }
            return render_json(result_dict)


# 编辑:弹出框定时任务保存
@csrf_exempt
def save_crontab(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        print task_id
        cron_min = request.POST.get('cron_min')
        cron_hour = request.POST.get('cron_hour')
        cron_day = request.POST.get('cron_day')
        cron_month = request.POST.get('cron_month')
        cron_week = request.POST.get('cron_week')
        cron_task = request.POST.get('cron_task')
        operator = get_login_user(request)  # 操作人: 当前登录用户
        try:
            # 查出编辑前的定时任务
            obj = CrontabInfo.objects.get(id=task_id)
            edit_data = {
                "operator":operator,
                "cron_task_before":obj.cron_min + " " + obj.cron_hour + " " + obj.cron_day + " " + obj.cron_month+ " "+ obj.cron_week + " " +obj. cron_task,
                "cron_task_after": cron_min + " " + cron_hour + " " + cron_day + " " + cron_month+ " "+ cron_week + " " + cron_task,
                "operation": 2,
                "cron_info_id":task_id,
            }
            # 任务变更表:追加变更记录
            CrontabChangeHistory.objects.create(**edit_data)
            # 任务表:更新操作人修改的任务
            new_cron = {
                "cron_min": cron_min,
                "cron_hour": cron_hour,
                "cron_day": cron_day,
                "cron_month": cron_month,
                "cron_week": cron_week,
                "cron_task": cron_task,
                }
            CrontabInfo.objects.create(**new_cron)
            # 同步至服务器
            sync_to_server(request, task_id)
            result = {'result': True, 'message': u"保存任务成功"}
        except Exception as e:
            result = {'result': False, 'message': u"保存任务失败,%s" % e}
            logger.info("edit_crontab, result: %s." % traceback.format_exc(e))
        return render_json(result)


# 删除定时任务
@csrf_exempt
def delete_crontab(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        print task_id
        try:
            operator = get_login_user(request)  # 操作人: 当前登录用户
            CrontabInfo.objects.filter(id=task_id).update(deleted='1')
            obj = CrontabInfo.objects.get(id=task_id)
            # print obj
            data = {
                "operator": operator,
                "operation": 1,
                "cron_task_before": obj.cron_min + " " + obj.cron_hour + " " + obj.cron_day + " " + obj.cron_month + " " + obj.cron_week + " " + obj.cron_task,
                "cron_task_after": " ",
                "cron_info_id": task_id,
                }
            CrontabChangeHistory.objects.create(**data)
            sync_to_server(request, task_id)  # 同步至服务器
            result = {'result': True, 'message': u"删除任务成功" }
        except Exception as e:
            result = {'result': False, 'message': u"删除任务失败,%s" % e}
            logger.info("delete_crontab, result: %s." % traceback.format_exc(e))
        return render_json(result)


# 查询编辑详情
@csrf_exempt
def get_edit_detail(request):
    if request.method == 'POST':
        task_id = request.POST.get("id",None)
        print "task_id%s" % task_id
        # task_id = 1216
        obj = CrontabChangeHistory.objects.filter(cron_info_id=task_id)
        if len(obj) == 0:
            return render_json(" ")
        elif len(obj) == 1:
            edit_detail = {
                "operator": obj.operator,
                "operation": obj.operation,
                "cron_task_before": obj.cron_task_before,
                "cron_task_after": obj.cron_task_after,
                "last_edit_time":obj.last_edit_time,
             }
            print edit_detail
        else:
            detail_list = []
            for item in obj:
                detail_dict ={
                    "operator": item.operator,
                    "operation":  item.operation,
                    "cron_task_before": item.cron_task_before,
                    "cron_task_after": item.cron_task_after,
                    "last_edit_time": str(item.last_edit_time),
                    }
                detail_list.append(detail_dict)
            print "detail_list%s" % detail_list
            return render_json(detail_list)


# 编辑/删除定时任务同步到服务器
def sync_to_server(request,task_id):
    # 获取当前业务的ID
    # task_id =1559
    obj = BusinessInfo.objects.get(current_biz=1)
    bk_biz_id = obj.bk_biz_id
    cron_obj = CrontabInfo.objects.get(id=task_id)
    ip = cron_obj.server_ip
    user = cron_obj.creator
    # 调用快速执行脚本,先清空用户的现有定时任务
    clear_cron = "echo ' ' >/var/spool/cron/{user}"
    clear_cron_script = clear_cron.format(user=user)
    script_content = base64_encode(clear_cron_script)
    # print script_content
    # 执行脚本
    kwargs = {
        "bk_biz_id": bk_biz_id,
        "script_content": script_content,
        "script_type": 1,
        "account": "root",
        "ip_list": [
            {"bk_cloud_id": 0, "ip": ip}, ], }
    execute_script(request, kwargs)
    # 查询出本地库里未删除的改用户的定时任务
    query_result = CrontabInfo.objects.filter(Q(creator=user) & Q(deleted=0))
    crontab_list = []
    for c in query_result:
        crontab_list.append(c.cron_min+" "+c.cron_hour+" "+c.cron_day+" "+c.cron_month+" "+c.cron_week+" "+c.cron_task)
    crontab = "echo" + " " + "'{cron_time}'" + ">> /var/spool/cron/{user}"+"\n"
    # 调用执行脚本逐条追加到服务器某个用户的定时任务文件里
    for cron in crontab_list:
        script = crontab.format(cron_time=cron,user=user)
        # print "script%s" % script
        script_content = base64_encode(script)
        kwargs = {
            "bk_biz_id": bk_biz_id,
            "script_content": script_content,
            "script_type": 1,
            "account": "root",
            "ip_list": [
                {"bk_cloud_id": 0, "ip": ip}, ], }
        execute_script(request, kwargs)


# 启动定时任务
def start_crontab(request):
    if request.method == 'POST':
        task_id = request.GET.get('task_id')
        try:
            CrontabInfo.objects.filter(id=task_id).update(status='1')
            result = {'result': True, 'message': u"start a crontab successfully"}
        except Exception as e:
            result = {'result': False, 'message': u"fail to start a crontab,%s" % e}
            logger.info("start_crontab, result: %s." % traceback.format_exc(e))
        return render_json(result)


# 快速执行脚本
def execute_script(request, kwargs):
    # client = get_client_by_request(request)
    user = "admin"
    client = get_client_by_user(user)
    execute_result = client.job.fast_execute_script(kwargs)
    # print execute_result
    time.sleep(3)
    job_instance_id = execute_result["data"].get("job_instance_id")
    # print job_instance_id
    parms = {
        "bk_biz_id": kwargs.get("bk_biz_id"),
        "job_instance_id": job_instance_id
    }
    jog_result = client.job.get_job_instance_log(parms)
    # print jog_result
    step_results = jog_result["data"][0].get("step_results")
    # print step_results
    ip_logs = step_results[0].get("ip_logs")
    # print ip_logs
    log_content = ip_logs[0].get('log_content')
    # print log_content
    return log_content


# 服务器IP
@csrf_exempt
def search_bk_host(request):
    # client = get_client_by_request(request)
    # result = client.cc.search_host()
    user = "admin"
    client = get_client_by_user(user)
    obj = BusinessInfo.objects.get(current_biz=1)
    # 根据当前业务ID展示服务器列表
    bk_biz_id = obj.bk_biz_id
    # print bk_biz_id
    param ={"bk_biz_id":bk_biz_id}
    result = client.cc.search_host(param)
    info = result["data"].get("info")
    bk_host_innerip = []
    for i in info:
        bk_host_innerip.append(i["host"].get("bk_host_innerip"))
    return bk_host_innerip
    # return render_json(bk_host_innerip)


# Base64加密
def base64_encode(s):
    a = base64.b64encode(s)
    return a


# 获取当前登录用户
@csrf_exempt
def get_login_user(request):
    user = "admin"
    client = get_client_by_user(user)
    result = client.bk_login.get_user()
    bk_username = result["data"].get("bk_username")
    # print bk_username
    # return render_json(bk_username)
    return bk_username


