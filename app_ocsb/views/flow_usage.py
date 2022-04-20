""" view for workflow Syrup_Usage """
from django.shortcuts import get_object_or_404, redirect

from app_ocsb.models import SyrupUsage


def flow_draf_view(request, usage_id):
    """ change state from Draft to Review_1 """
    query_object = get_object_or_404(SyrupUsage, pk=usage_id)
    query_object.flow_draft()
    query_object.save()
    return redirect('syrubusage-list')

def flow_reviewed_1_view(request, usage_id):
    """ change state from Review_1 to Review_2 """
    query_object = get_object_or_404(SyrupUsage, pk=usage_id)
    query_object.flow_reviewed_1()
    query_object.save()
    return redirect('syrubusage-list')

def flow_reviewed_2_view(request, usage_id):
    """ change state from Review_2 to Review_3 """
    query_object = get_object_or_404(SyrupUsage, pk=usage_id)
    query_object.flow_reviewed_2()
    query_object.save()
    return redirect('syrubusage-list')

def flow_reviewed_3_view(request, usage_id):
    """ change state from Review_3 to Review_4 """
    query_object = get_object_or_404(SyrupUsage, pk=usage_id)
    query_object.flow_reviewed_3()
    query_object.save()
    return redirect('syrubusage-list')

def flow_reviewed_4_view(request, usage_id):
    """ change state from Review_4 to Review_5 """
    query_object = get_object_or_404(SyrupUsage, pk=usage_id)
    query_object.flow_reviewed_4()
    query_object.save()
    return redirect('syrubusage-list')

def flow_reviewed_5_view(request, usage_id):
    """ change state from Review_5 to Confirm """
    query_object = get_object_or_404(SyrupUsage, pk=usage_id)
    query_object.flow_reviewed_5()
    query_object.save()
    return redirect('syrubusage-list')

def flow_reject_view(request, usage_id):
    """ change state from Review to Reject """
    query_object = get_object_or_404(SyrupUsage, pk=usage_id)
    query_object.flow_reject()
    query_object.save()
    return redirect('syrubusage-list')
