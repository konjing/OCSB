""" Form for app_ocsb"""
from django.forms import ModelForm
from django_select2 import forms as s2forms
from app_ocsb.models import QuotaRequest


class PurchaserWidget(s2forms.ModelSelect2MultipleWidget):
    """ select 2 widget for Purchaser """
    search_fields = [
        "name__icontains",
        ]

class RequestFormStep1(ModelForm):
    """ Step1: Create/Draft Quota Request Form """
    class Meta:
        """ Meta Form """
        model = QuotaRequest
        fields = [  'user', 'date_request', 'enterprise', 'no_enterprise', \
        'no_request', 'total_syrup', 'total_cmolasses', 'is_season', \
        'season', 'total_bmolasses', 'total_amount', 'purchasers', \
        'file_request', 'file_sitevisit', 'file_survey', 'file_approve'
        ]
        widget = {
            "purchasers": PurchaserWidget,
        }
