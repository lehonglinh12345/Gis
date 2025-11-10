
# Register your models here.
from django.contrib import admin
from .models import Accident

@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    list_display = ['location', 'accident_type', 'damage_level', 'district', 'datetime']
    list_filter = ['accident_type', 'damage_level', 'district', 'datetime']
    search_fields = ['location']
    # date_hierarchy = 'datetime'
    ordering = ['-datetime']
    
    fieldsets = (
        ('Thông tin vị trí', {
            'fields': ('location', 'latitude', 'longitude', 'district')
        }),
        ('Thông tin tai nạn', {
            'fields': ('accident_type', 'damage_level', 'datetime')
        }),
    )