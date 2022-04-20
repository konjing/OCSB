""" Form for Request Quota """
from django import forms
from app_ocsb.models import QuotaRequest

class CreateRequestForm(forms.Form):
    """ ฟอร์มสร้างคำขออนุญาตฯ จากสถานประกอบการ """
    