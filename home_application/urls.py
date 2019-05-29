# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^cron_history/', 'cron_history'),
    (r'^get_biz$', 'get_biz'),
    (r'^get_current_biz', 'get_current_biz'),
   (r'^get_server_list$', 'get_server_list'),
    (r'^get_crontab_users$', 'get_crontab_users'),
    (r'^create_crontab$', 'create_crontab'),
    (r'^edit_crontab$', 'edit_crontab'),
   (r'^save_crontab$', 'save_crontab'),
    (r'^delete_crontab$', 'delete_crontab'),
    (r'^get_server_crontab$', 'get_server_crontab'),
    (r'^start_crontab$', 'start_crontab'),
    # (r'^get_execute_result/$', 'get_execute_result'),
   (r'^search_crontabs$', 'search_crontabs'),
    (r'^sync_to_server$', 'sync_to_server'),
    (r'^update_to_server/$', 'update_to_server'),
    (r'^select_server/$', 'select_server'),
    (r'^get_edit_detail$', 'get_edit_detail'),
    (r'^search_bk_host', 'search_bk_host'),
)
