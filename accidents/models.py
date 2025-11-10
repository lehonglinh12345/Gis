from django.db import models
from django.utils import timezone

class Accident(models.Model):
    ACCIDENT_TYPES = [
        ('xe_may', 'Tai nạn xe máy'),
        ('o_to', 'Tai nạn ô tô'),
        ('xe_tai', 'Tai nạn xe tải'),
        ('nguoi_di_bo', 'Tai nạn người đi bộ'),
        ('khac', 'Loại khác'),
    ]
    
    DAMAGE_LEVELS = [
        ('nhe', 'Nhẹ'),
        ('trung_binh', 'Trung bình'),
        ('nang', 'Nặng'),
        ('rat_nang', 'Rất nặng'),
    ]

    location = models.CharField(max_length=255, verbose_name='Điểm tai nạn')
    latitude = models.FloatField(verbose_name='Vĩ độ')
    longitude = models.FloatField(verbose_name='Kinh độ')
    accident_type = models.CharField(max_length=50, choices=ACCIDENT_TYPES, verbose_name='Loại tai nạn')
    datetime = models.DateTimeField(default=timezone.now, verbose_name='Thời gian')
    damage_level = models.CharField(max_length=50, choices=DAMAGE_LEVELS, verbose_name='Mức độ thiệt hại')

    # MỚI: Mã phường/xã (maXa) - DÙNG CHO TOÀN QUỐC
    commune_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Mã Phường/Xã',
        help_text="Ví dụ: 81519002"
    )

    class Meta:
        db_table = 'accidents'
        verbose_name = 'Vụ tai nạn'
        verbose_name_plural = 'Các vụ tai nạn'
        ordering = ['-datetime']
    
    def __str__(self):
        return f"{self.location} - {self.get_accident_type_display()}"