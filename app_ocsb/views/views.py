""" View app_ocsb """
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
import sweetify

from app_ocsb.form.form import RequestFormStep1
from app_ocsb.form.form_request import RequestFormFile
from app_ocsb.models import QuotaRequest, SyrupUsage
from app_base.models import Purchaser
from app_base.decorators import allowed_users


# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer'])
def request_index_view(request):
    """ View for Index Quota Request """
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.all()[0].name
        user_enterprise = request.user.user_profile.enterprises.all()
        enterprise_list = []
        for record in user_enterprise:
            enterprise_list.append(record.id) #ใส่ enterprise_id ทั้งหมดเข้า enterprise_list
        # กรองการแสดงรายการคำขอฯ
        if user_group == 'admin': #ทุกรายการ
            queryset = QuotaRequest.objects.filter(season__is_active=True)
        elif user_group == 'ent_officer': #กลุ่มเจ้าหน้าที่โรงงาน
            queryset = QuotaRequest.objects.filter(enterprise__in=enterprise_list)\
                .filter(season__is_active=True)
        else:
            return redirect('home')

    else:
        return redirect('home')

    context = {'queryset': queryset}
    return render(request, 'app_ocsb/request_index.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer'])
def request_create_view(request):
    """ View for Create Quota Request """
    form = RequestFormStep1()
    form.user = request.user.id
    if request.method == 'POST':
        form = RequestFormStep1(request.POST, request.FILES)
        # form.no_request = QuotaRequest.generate_no_request(QuotaRequest, season)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'สร้างคำขออนุญาตฯ สำเร็จ')
            return redirect('request-list')

    user_group = request.user.groups.all()[0].name
    user_enterprise = request.user.user_profile.enterprises.all()[0]
    context = {'form':form, 'user_group': user_group, 'user_enterprise': user_enterprise}
    return render(request, 'app_ocsb/request_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ocsb_officer', 'ent_officer'])
def request_list_view(request):
    """ View for request List """
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.all()[0].name
        user_enterprise = request.user.user_profile.enterprises.all()
        enterprise_list = []
        for record in user_enterprise:
            enterprise_list.append(record.id) #ใส่ enterprise_id ทั้งหมดเข้า enterprise_list
        # กรองการแสดงรายการคำขอฯ
        if user_group == 'admin': #ทุกรายการ
            queryset = QuotaRequest.objects.all()
        elif user_group == 'ent_officer': #ตามกลุ่มผู้ใช้ สถานะ และสปก.
            queryset = QuotaRequest.objects.filter(workflow_state__in=[0]).\
                filter(enterprise__in=enterprise_list)
        elif user_group == 'ocsb_officer': #ตามกลุ่มผู้ใช้ สถานะ
            queryset = QuotaRequest.objects.filter(workflow_state__in=[1, 2, 3]).\
                filter(enterprise__in=enterprise_list)
        else:
            return redirect('home')

    else:
        return redirect('home')

    context = {'queryset': queryset}
    return render(request, 'app_ocsb/request_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ocsb_officer', 'ent_officer'])
def request_detail_view(request, request_id):
    """ Show Request Detail """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    query_usage = SyrupUsage.objects.filter(quota_request=request_id).order_by('date_report')
    purchaser_object = Purchaser.objects.filter(quotarequest__id=request_id)
    workflow_state = query_object.workflow_state
    user_group = request.user.groups.all()[0].name
    form = RequestFormFile(instance=query_object)

    if request.method == 'POST':
        form = RequestFormFile(request.POST, request.FILES, instance=query_object)
        if form.is_valid():
            form.save()
            return redirect('request-detail', request_id=request_id)

    context = {
        'query_object': query_object,
        'query_usage': query_usage,
        'purchaser_object': purchaser_object,
        'workflow_state': workflow_state,
        'request_id': request_id,
        'user_group':user_group,
        'form': form,
        }
    return render(request, 'app_ocsb/request_detail.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ocsb_officer', 'ent_officer'])
def request_update_view(request, request_id):
    """ Update Quota Request """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    workflow_state = query_object.workflow_state
    form = RequestFormStep1(instance=query_object)

    if request.method == 'POST':
        form = RequestFormStep1(request.POST, request.FILES, instance=query_object)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'แก้ไขคำขออนุญาตฯ สำเร็จ')
            return redirect('request-detail')

    user_group = request.user.groups.all()[0].name
    user_enterprise = request.user.user_profile.enterprises.all()[0]
    context = {
        'form': form, 'request_id': request_id, 'workflow_state': workflow_state,
        'user_group': user_group, 'user_enterprise': user_enterprise}
    return render(request, 'app_ocsb/request_form.html', context)
