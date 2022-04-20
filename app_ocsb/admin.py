""" Admin Page app_ocsb """
from django.contrib import admin
from app_ocsb.models import QuotaRequest, SyrupUsage

# Register your models here.
admin.site.register(SyrupUsage)

@admin.register(QuotaRequest)
class QuotaRrquestAdmin(admin.ModelAdmin):
    """ Config display QuotaRrquest in AdminPage """
    list_display = ['no_request', 'user', 'enterprise', 'workflow_state']
    list_filter = ['enterprise']
