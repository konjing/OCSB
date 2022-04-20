""" Admin Page """
from django.contrib import admin
from app_base.models import Region, Province, Amphur, Tumbol,\
    Enterprise, Season, Profile, Purchaser, Brix

# Register your models here.
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(Amphur)
admin.site.register(Tumbol)
admin.site.register(Enterprise)
admin.site.register(Profile)
admin.site.register(Purchaser)

@admin.register(Brix)
class BrixAdmin(admin.ModelAdmin):
    """ Config display in AdminPage """
    list_display = ['brix_value', 'spcific_gravity']
    list_filter = ['brix_value']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    """ Config display in AdminPage """
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active']
