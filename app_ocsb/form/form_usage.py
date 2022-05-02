""" SyrubUsage Form """
from django import forms
from app_base.models import Purchaser

from app_ocsb.models import SyrupUsage


class SyrupUsageForm(forms.ModelForm):
    """ Syrub Form """
    class Meta:
        """ Meta Data"""
        model = SyrupUsage
        fields = [
            'quota_request', 'enterprise', #hidden, initial
            # กรอกข้อมูล
            'date_report', 'purchaser', 'syrup_type',
            'syrup_valume', 'syrup_weight', 'theoretical', 'undetermine_loss',
            'syrup_brix', 'syrup_pol',
            'rawsugar_moisture', 'rawsugar_pol',
            'mollasses_brix', 'mollasses_pol',
            'daily_cane_input', 'pol_in_can', 'pol_extraction', 'loss_filter_cake',
            # คำนวณ (มีใน Form)
            'syrup_purity', 'rawsugar_purity', 'mollasses_purity',
            'sjm', 'actual_sugar_recovery','raw_sugar_tons_pol',
            'raw_sugar_tons', 'ton_mollasses',
            ### คำนวณ (ไม่มีมีใน Form)
            #'ton_pol_syrup', 'ton_pol_rawsuger', 'ton_under_loss','ton_pol_mollasses',
            #'ton_pol_daily', 'ton_pol_mixed', 'ton_pol_filter',
            #'ton_pol_clearified', 'ton_raw_syrup', 'ratio_raw_cane',
            #'estimate_ton_can', 'efficiency_raw', 'efficiency_mollasses',
            #'density_indice',
            ### คำนวณ (รอคุณหน่องแจ้งอีกที)
            #'raw_sugar_tons_ent', 'ton_mollasses_ent', 'diff_raw_sugar', 'diff_ton_mollasses',
            ]
        widgets = {
            'quota_request': forms.HiddenInput(),
            'enterprise': forms.HiddenInput(),
            'date_report': forms.DateInput(
                format=('%Y-%m-%d')
            ),
        }

    def __init__(self, request_id, *args, **kwargs):
        super(SyrupUsageForm, self).__init__(*args, **kwargs)
        self.fields['purchaser'].queryset = Purchaser.objects.filter(quotarequest__id=request_id)
