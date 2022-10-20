""" View for DashBoard """
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from app_base.decorators import allowed_users
from app_ocsb.models import QuotaRequest, SyrupUsage

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer', 'ocsb_officer'])
def dashboard_ent_view(request):
    """ View for Enterprise Dashboard """
    user_enterprise = request.user.user_profile.enterprises.all()[0].id
    # queryset Show only QuotaRequest is Active & status=Accept
    queryset = QuotaRequest.objects.filter(enterprise=user_enterprise)\
        .filter(is_active=1).filter(workflow_state=4)
    queryset_usage = SyrupUsage.objects.filter(enterprise=user_enterprise)\
        .filter(is_active=1).order_by('create_date')[:10]
    queryset_sum_usage = SyrupUsage.objects.filter(enterprise=user_enterprise)\
        .values('purchaser__name')\
        .annotate(Sum('syrup_weight'))

    context = {
        'queryset': queryset, 'queryset_usage': queryset_usage,
        'queryset_sum_usage': queryset_sum_usage}
    return render(request, 'app_ocsb/dashboard_ent.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer', 'ocsb_officer'])
def dashboard_ocsb_view(request):
    """ View for OCSB_Officer Dashboard """
    queryset = QuotaRequest.objects.filter(is_active=1)
    queryset_usage = SyrupUsage.objects\
        .filter(is_active=1).order_by('create_date')
    queryset_sum_usage = SyrupUsage.objects.values('purchaser__name')\
        .annotate(Sum('syrup_weight')).order_by('-syrup_weight__sum')
    queryset_sum_enterprise = SyrupUsage.objects.values('enterprise__name')\
        .annotate(Sum('syrup_weight')).order_by('-syrup_weight__sum')

    context = {
        'queryset': queryset, 'queryset_usage': queryset_usage,
        'queryset_sum_usage': queryset_sum_usage,
        'queryset_sum_enterprise': queryset_sum_enterprise}
    return render(request, 'app_ocsb/dashboard_ocsb.html', context)
