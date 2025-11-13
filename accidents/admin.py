from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Accident


# === Helper: Hành động export CSV ===
def export_as_csv(modeladmin, request, queryset):
    """
    Cho phép xuất danh sách vụ tai nạn đã chọn ra file CSV.
    """
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
    writer = csv.writer(response)

    # Ghi header
    writer.writerow(field_names)

    # Ghi từng dòng dữ liệu
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response
export_as_csv.short_description = "📤 Xuất các vụ đã chọn ra CSV"


# === Admin chính cho model Accident ===
@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    # Hiển thị cột trong trang danh sách
    list_display = (
        'id',
        'location',
        'accident_type',
        'damage_level',
        'commune_code',
        'datetime',
        'latitude',
        'longitude',
    )

    # Các trường được phép tìm kiếm
    search_fields = ('location', 'commune_code', 'accident_type', 'damage_level')

    # Bộ lọc nhanh bên phải
    list_filter = ('accident_type', 'damage_level', 'commune_code', 'datetime')

    # Hiển thị lịch theo ngày ở trên cùng
    date_hierarchy = 'datetime'

    # Cho phép xuất CSV
    actions = [export_as_csv]

    # Sắp xếp mặc định: mới nhất trước
    ordering = ['-datetime']

    # Giới hạn số dòng mỗi trang
    list_per_page = 50

    # Chia form chỉnh sửa thành các nhóm
    fieldsets = (
        ('Thông tin chính', {
            'fields': ('location', 'commune_code', 'accident_type', 'damage_level')
        }),
        ('Vị trí địa lý', {
            'fields': ('latitude', 'longitude'),
            'description': 'Vĩ độ (latitude) và Kinh độ (longitude) của vụ tai nạn'
        }),
        ('Thời gian', {
            'fields': ('datetime',),
        }),
    )

    # Tùy chỉnh hiển thị readable cho loại và mức độ tai nạn
    def accident_type_display(self, obj):
        return obj.get_accident_type_display()
    accident_type_display.short_description = 'Loại tai nạn'

    def damage_level_display(self, obj):
        return obj.get_damage_level_display()
    damage_level_display.short_description = 'Mức độ'

