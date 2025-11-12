import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from .models import Accident
from .forms import AccidentForm, AccidentSearchForm, AccidentFilterForm
from datetime import datetime, timedelta
from django.utils import timezone

def dashboard(request):
    context = {
        'add_form': AccidentForm(),
        'search_form': AccidentSearchForm(),
        'filter_form': AccidentFilterForm(),
    }
    return render(request, 'accidents/dashboard.html', context)

def add_accident(request):
    if request.method == 'POST':
        form = AccidentForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, 'Thêm thành công!')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            messages.error(request, 'Lỗi form.')
    return redirect('index')

# --- API: LẤY DANH SÁCH TAI NẠN ---
def api_get_accidents(request):
    # accidents = Accident.objects.all()
    now = timezone.now()
    one_day_ago = now - timedelta(days=1)

    accidents = Accident.objects.filter(
        datetime__gte=one_day_ago
    )
    # Lọc
    accident_type = request.GET.get('accident_type')
    damage_level = request.GET.get('damage_level')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if accident_type: accidents = accidents.filter(accident_type=accident_type)
    if damage_level: accidents = accidents.filter(damage_level=damage_level)

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            accidents = accidents.filter(datetime__range=[start_datetime, end_datetime])
        except ValueError:
            pass

    accidents_data = []
    for acc in accidents:
        accidents_data.append({
            'id': acc.id,
            'location': acc.location,
            'lat': acc.latitude,
            'lng': acc.longitude,
            'type': acc.accident_type,
            'type_display': acc.get_accident_type_display(),
            'datetime': acc.datetime.strftime('%d/%m/%Y %H:%M'),
            'damage': acc.get_damage_level_display(),
            'damage_slug': acc.damage_level,
            'commune_code': acc.commune_code,
        })
    
    return JsonResponse({'accidents': accidents_data})

# --- API: THỐNG KÊ THEO PHƯỜNG/XÃ (maXa) ---
def api_get_statistics(request):
    accidents = Accident.objects.all()
    
    
    # Áp dụng lọc
    accident_type = request.GET.get('accident_type')
    damage_level = request.GET.get('damage_level')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if accident_type: accidents = accidents.filter(accident_type=accident_type)
    if damage_level: accidents = accidents.filter(damage_level=damage_level)
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            accidents = accidents.filter(datetime__range=[start_datetime, end_datetime])
        except ValueError:
            pass

    # THỐNG KÊ THEO maXa
    commune_stats = accidents.values('commune_code').annotate(count=Count('id')).order_by('-count')

    labels = []
    counts = []
    stats_map = {}

    for item in commune_stats:
        code = item['commune_code']
        if not code:
            continue
        count = item['count']
        labels.append(code)
        counts.append(count)
        stats_map[code] = count  # { "81519002": 5 }

    return JsonResponse({
        'chart_data': {
            'labels': labels,
            'counts': counts
        },
        'stats_map': stats_map
    })


# API: LẤY GEOJSON THEO TỈNH
def api_get_geojson_by_province(request):
    province = request.GET.get('province')
    if not province:
        return JsonResponse({'error': 'Thiếu province'}, status=400)

    # SỬA: DÙNG ĐƯỜNG DẪN ĐÚNG TRONG DJANGO
    geojson_path = os.path.join(settings.BASE_DIR, 'accidents', 'static', 'geojson', 'DiaPhan_Xa_2025.geojson')
    
    try:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return JsonResponse({'error': 'Không tìm thấy file GeoJSON'}, status=500)

    filtered = {
        'type': 'FeatureCollection',
        'features': [
            f for f in data['features']
            if f['properties'].get('tenTinh') == province
        ]
    }
    return JsonResponse(filtered)