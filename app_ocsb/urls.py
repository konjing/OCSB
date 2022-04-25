""" app_ocsb urls """
from django.urls import path

from app_ocsb.views.views import request_create_view, request_index_view,\
    request_list_view, request_detail_view, request_update_view
from app_ocsb.views import syrup_usage as usage
from app_ocsb.views import flow_request as flow_re
from app_ocsb.views import flow_usage as flow_us
from app_ocsb.views import dashboard_view as db
from app_ocsb.views import report_view as report

urlpatterns = [
    path('', db.dashboard_ent_view, name='home'),
    # ------------------- Dash Board ----------
    path('dashboard-ent/', db.dashboard_ent_view, name='dashboard-ent'),
    path('dashboard-ocsb/', db.dashboard_ocsb_view, name='dashboard-ocsb'),
    # ------------------- RequestQuota ----------
    path('request-index/', request_index_view, name='request-index'),
    path('request-form/', request_create_view, name='request-form'),
    path('request-list/', request_list_view, name='request-list'),
    path('request-detail/<int:request_id>',
         request_detail_view, name='request-detail'),
    path('request-update/<int:request_id>',
         request_update_view, name='request-update'),
    # ------------------- Change State for RequestQuota ----------
    path('request-state-sent/<int:request_id>',
         flow_re.flow_sent_view, name='request-state-sent'),
    path('request-state-reviewed-new/<int:request_id>',
         flow_re.flow_reviewed_new_view, name='request-state-reviewed-new'),
    path('request-state-reviewed-old/<int:request_id>',
         flow_re.flow_reviewed_old_view, name='request-state-reviewed-old'),
    path('request-state-sitevisit/<int:request_id>',
         flow_re.flow_sitevisit_view, name='request-state-sitevisit'),
    path('request-state-accept/<int:request_id>',
         flow_re.flow_accept_view, name='request-state-accept'),
    path('request-state-reject/<int:request_id>',
         flow_re.flow_reject_view, name='request-state-reject'),
    path('request-state-close/<int:request_id>',
         flow_re.flow_close_view, name='request-state-close'),
    # ------------------- SyrubUsage ----------
    path('usage-list/', usage.list_usage_view, name='usage-list'),
    path('syrubusage-list/', usage.list_syrubusage_view, name='syrubusage-list'),
    path('usage-form/<int:request_id>', usage.create_usage_view, name='usage-form'),
    path('usage-update/<int:usage_id>', usage.update_usage_view, name='usage-update'),
    path('usage-detail/<int:usage_id>', usage.detail_usage_view, name='usage-detail'),
    # ------------------- Change State for SyrubUsage ----------
    path('usage-state-draft/<int:usage_id>',
         flow_us.flow_draf_view, name='usage-state-draft'),
    path('usage-state-review1/<int:usage_id>',
         flow_us.flow_reviewed_1_view, name='usage-state-review1'),
    path('usage-state-review2/<int:usage_id>',
         flow_us.flow_reviewed_2_view, name='usage-state-review2'),
    path('usage-state-review3/<int:usage_id>',
         flow_us.flow_reviewed_3_view, name='usage-state-review3'),
    path('usage-state-review4/<int:usage_id>',
         flow_us.flow_reviewed_4_view, name='usage-state-review4'),
    path('usage-state-review5/<int:usage_id>',
         flow_us.flow_reviewed_5_view, name='usage-state-review5'),
    path('usage-state-reject/<int:usage_id>',
         flow_us.flow_reject_view, name='usage-state-reject'),
    # ------------------- Change State for SyrubUsage ----------
    path('report-usage-01/', report.report_usage_1, name='report-usage-01'),
    path('report-usage-02/', report.report_usage_2, name='report-usage-02'),
    path('report-usage-03/', report.report_usage_3, name='report-usage-03'),
]
