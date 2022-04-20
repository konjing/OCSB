""" view for workflow request """
from django.shortcuts import get_object_or_404, redirect

from app_ocsb.models import QuotaRequest


def flow_sent_view(request, request_id):
    """ change state from Draft to Review """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    query_object.flow_sent()
    query_object.save()
    return redirect('request-list')

def flow_reviewed_new_view(request, request_id):
    """ change state from Review to SiteVisit """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    query_object.flow_reviewed_new()
    query_object.save()
    return redirect('request-list')

def flow_reviewed_old_view(request, request_id):
    """ change state from Review to Approval กรณีเป็นการขอเพิ่ม """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    query_object.flow_reviewed_old()
    query_object.save()
    return redirect('request-list')

def flow_sitevisit_view(request, request_id):
    """ change state from SiteVisit to Approval """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    query_object.flow_sitevisit()
    query_object.save()
    return redirect('request-list')

def flow_accept_view(request, request_id):
    """ change state from Approval to Accept """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    query_object.flow_accept()
    query_object.save()
    return redirect('request-list')

def flow_reject_view(request, request_id):
    """ change state from Approval to Reject """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    query_object.flow_reject()
    query_object.save()
    return redirect('request-list')

def flow_close_view(request, request_id):
    """ change state from Accept to Close """
    query_object = get_object_or_404(QuotaRequest, pk=request_id)
    query_object.flow_close()
    query_object.save()
    return redirect('request-list')
