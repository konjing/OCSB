""" View for Report """
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from app_base.decorators import allowed_users
from app_ocsb.models import SyrupUsage

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer', 'ocsb_officer'])
def report_usage_1(request):
    """ รายงานการจำหน่ายน้ำเชื่อมประจำเดือน """
    queryset = SyrupUsage.objects.all()
    context = {'queryset': queryset}
    return render(request, 'app_ocsb/report/report_usage01.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer', 'ocsb_officer'])
def report_usage_2(request):
    """ รายงานการจำหน่ายน้ำเชื่อมประจำเดือน แบ่งตามโรงงานผลิตน้ำตาล (จำหน่าย) """
    queryset = SyrupUsage.objects.values('enterprise__name', 'syrup_type')\
        .annotate(Sum('syrup_weight'))
    context = {'queryset': queryset}
    return render(request, 'app_ocsb/report/report_usage02.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer', 'ocsb_officer'])
def report_usage_3(request):
    """ รายงานการจำหน่ายน้ำเชื่อมประจำเดือน แบ่งตามโรงงานผลิตเอทานอล (รับซื้อ) """
    queryset = SyrupUsage.objects.values('purchaser__name', 'syrup_type')\
        .annotate(Sum('syrup_weight'))
    context = {'queryset': queryset}
    return render(request, 'app_ocsb/report/report_usage03.html', context)
