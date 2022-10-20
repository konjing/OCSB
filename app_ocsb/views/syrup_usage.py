""" View for Syrub Usage """
from datetime import datetime
from decimal import Decimal
from math import floor
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from app_ocsb.form.form_usage import SyrupUsageForm
from app_ocsb.models import QuotaRequest, SyrupUsage
from app_base.models import Brix
from app_base.decorators import allowed_users


# Create your views here
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer'])
def list_usage_view(request):
    """ Show Request list (Active) """
    user_enterprise = request.user.user_profile.enterprises.all()
    enterprise_list = []
    for record in user_enterprise:
        enterprise_list.append(record.id)
    # แสดงเฉพาะคำขอฯที่สถานะ Accept และเป็น สปก. เดียวกัน
    queryset = QuotaRequest.objects\
        .filter(workflow_state=4).filter(enterprise__in=enterprise_list)
    context = {'queryset': queryset}
    return render(request, 'app_ocsb/usage_list.html', context)


@login_required(login_url='login')
@allowed_users(
    allowed_roles=['admin', #เจ้าหน้าที่ ดูแลระบบ
                   'ent_officer', #เจ้าหน้าที่ โรงงานน้ำตาล
                   'ocsb_officer', #เจ้าหน้าที่ เจ้าหน้าที่ สอน.
                   'district_officer', #เจ้าหน้าที่ เขต
                   'sugarzone_officer', #เจ้าหน้าที่ สบน.
                   'bio_officer' #เจ้าหน้าที่ กสช.
                   ]
)
def list_syrubusage_view(request):
    """ Show Usage Syrub list """
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.all()[0].name
        user_enterprise = request.user.user_profile.enterprises.all()
        enterprise_list = []
        for record in user_enterprise:
            enterprise_list.append(record.id)
        # กรองการแสดงรายการคำขอฯ
        if user_group == 'admin':  # ทุกรายการ
            queryset = SyrupUsage.objects.all()
        elif user_group == 'ent_officer':  # เจ้าหน้าที่บริษัท
            queryset = SyrupUsage.objects.filter(workflow_state__in=[0, 1, 6, 7]).\
                filter(enterprise__in=enterprise_list)
        elif user_group == 'ocsb_officer':  # เจ้าหน้าที่ สอน. ประจำโรงงาน
            queryset = SyrupUsage.objects.filter(workflow_state__in=[2]).\
                filter(enterprise__in=enterprise_list)
        elif user_group == 'district_officer':  # เจ้าหน้าที่ เขต
            queryset = SyrupUsage.objects.filter(workflow_state__in=[3]).\
                filter(enterprise__in=enterprise_list)
        elif user_group == 'sugarzone_officer':  # เจ้าหน้าที่ สบน.
            queryset = SyrupUsage.objects.filter(workflow_state__in=[4]).\
                filter(enterprise__in=enterprise_list)
        elif user_group == 'bio_officer':  # เจ้าหน้าที่ กสช.
            queryset = SyrupUsage.objects.filter(workflow_state__in=[5]).\
                filter(enterprise__in=enterprise_list)
        else:
            return redirect('home')

    else:
        return redirect('home')

    context = {'queryset': queryset}
    return render(request, 'app_ocsb/usagesyrub_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer'])
def create_usage_view(request, request_id):
    """ Create SyrubUsage """
    request_object = get_object_or_404(QuotaRequest, pk=request_id)
    initial = {
        'quota_request': request_object.id,
        'enterprise': request_object.enterprise,
        'date_report': datetime.today(),
        'theoretical': 100.00,
        'undetermine_loss': 0.00,
    }
    form = SyrupUsageForm(initial=initial, request_id=request_id)

    if request.method == 'POST':
        form = SyrupUsageForm(request_id=request_id, data=request.POST)
        if form.is_valid():
            # Save to table SyrupUsage
            syrup_usage = form.save(commit=False)

            # คำนวณ Density Indice
            floor_brix = round(Decimal(floor(syrup_usage.syrup_brix * 10)/10), 2)
            brix_bot = Brix.objects.get(brix_value=floor_brix)
            brix_top = Brix.objects.get(
                brix_value=(floor_brix + Decimal('0.1')))
            diff_gravity = brix_top.spcific_gravity - brix_bot.spcific_gravity
            diff_brix = (syrup_usage.syrup_brix - round(floor_brix, 2)) * 10
            diff_gravity_value = diff_gravity * diff_brix
            density_indice = brix_bot.spcific_gravity + diff_gravity_value

            syrup_usage.density_indice = round(density_indice, 5)
            syrup_usage.syrup_valume = round(
                syrup_usage.density_indice / syrup_usage.syrup_weight, 2)
            syrup_usage.ton_pol_syrup = round(
                syrup_usage.syrup_weight * syrup_usage.syrup_pol / 100, 2)
            syrup_usage.ton_pol_rawsuger = round(
                syrup_usage.raw_sugar_tons_pol, 2)
            syrup_usage.ton_under_loss = round(
                syrup_usage.undetermine_loss / 100 * syrup_usage.ton_pol_syrup, 2)
            syrup_usage.ton_pol_mollasses = round(
                syrup_usage.ton_pol_syrup - syrup_usage.ton_pol_rawsuger -
                syrup_usage.ton_under_loss, 2)
            syrup_usage.ton_mollasses = round(
                syrup_usage.ton_pol_mollasses / (syrup_usage.mollasses_pol/100), 2)
            syrup_usage.ton_pol_daily = round(
                syrup_usage.daily_cane_input * syrup_usage.pol_in_can / 100, 2)
            syrup_usage.ton_pol_mixed = round(
                syrup_usage.ton_pol_daily * syrup_usage.pol_extraction / 100, 2)
            syrup_usage.ton_pol_filter = round(
                syrup_usage.ton_pol_daily * syrup_usage.loss_filter_cake / 100, 2)
            syrup_usage.ton_pol_clearified = round(
                syrup_usage.ton_pol_mixed - syrup_usage.ton_pol_filter, 2)
            syrup_usage.ton_raw_syrup = round(
                syrup_usage.ton_pol_clearified / (syrup_usage.syrup_pol / 100), 2)
            syrup_usage.ratio_raw_cane = round(
                syrup_usage.ton_raw_syrup / syrup_usage.daily_cane_input, 4)
            if syrup_usage.ratio_raw_cane == 0.0000:
                syrup_usage.ratio_raw_cane = Decimal('0.01')
            syrup_usage.estimate_ton_can = round(
                syrup_usage.syrup_weight / syrup_usage.ratio_raw_cane, 2)
            syrup_usage.efficiency_raw = round(
                (syrup_usage.raw_sugar_tons * 1000) / syrup_usage.estimate_ton_can, 2)
            syrup_usage.efficiency_mollasses = round(
                (syrup_usage.ton_mollasses * 1000) / syrup_usage.estimate_ton_can, 2)
            syrup_usage.create_user = request.user
            syrup_usage.save()

            # ปรับปรุงตัวเลขการใช้น้ำเชื่อมในตาราง QuotaRequest
            total_syrup_before = request_object.total_usage_syrup
            total_bmolasses_before = request_object.total_usage_bmolasses
            total_cmolasses_before = request_object.total_usage_cmolasses

            usage_type = syrup_usage.syrup_type
            if usage_type == 1:  # Syrup
                total_syrup_after = total_syrup_before + syrup_usage.syrup_weight
                request_object.total_usage_syrup = total_syrup_after
                request_object.save()
            elif usage_type == 2:  # B-molasses
                total_bmolasses_after = total_bmolasses_before + syrup_usage.syrup_weight
                request_object.total_usage_bmolasses = total_bmolasses_after
                request_object.save()
            elif usage_type == 3:  # C-molasses
                total_cmolasses_after = total_cmolasses_before + syrup_usage.syrup_weight
                request_object.total_usage_cmolasses = total_cmolasses_after
                request_object.save()
            else:
                return HttpResponse('Not Select Type')

            return redirect('syrubusage-list')

    context = {'form': form, 'request_object': request_object}
    return render(request, 'app_ocsb/usage_form.html', context)


@login_required(login_url='login')
@allowed_users(
    allowed_roles=['admin', 'ent_officer', 'ocsb_officer', 'district_officer',
                   'sugarzone_officer', 'bio_officer'])
def detail_usage_view(request, usage_id):
    """ Detail Syrup Usage """
    usage_object = get_object_or_404(SyrupUsage, pk=usage_id)
    workflow_state = usage_object.workflow_state
    user_group = request.user.groups.all()[0].name

    context = {'usage_object': usage_object,
               'usage_id': usage_id,
               'workflow_state': workflow_state,
               'user_group': user_group
               }
    return render(request, 'app_ocsb/usage_detail.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'ent_officer'])
def update_usage_view(request, usage_id):
    """  Update Syrup Usage """
    usage_object = get_object_or_404(SyrupUsage, pk=usage_id)
    request_id = usage_object.quota_request.id
    request_object = get_object_or_404(QuotaRequest, pk=request_id)
    form = SyrupUsageForm(instance=usage_object, request_id=request_id)
    if request.method == 'POST':
        form = SyrupUsageForm(instance=usage_object,
                              request_id=request_id, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('syrubusage-list')

    context = {'form': form, 'request_object': request_object}
    return render(request, 'app_ocsb/usage_form.html', context)
