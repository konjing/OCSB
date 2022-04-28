""" Form for Request Quota """
from django.forms import ModelForm
from app_ocsb.models import QuotaRequest

class RequestFormFile(ModelForm):
    """ Upload File : Request Form """
    class Meta:
        """ Meta Form """
        model = QuotaRequest
        fields = [
            'file_request', 'file_sitevisit', 'file_survey', 'file_approve'
        ]
