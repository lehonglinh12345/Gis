from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import Accident
from .forms import AccidentForm, SearchForm, FilterForm
import json

def index(request):
    """Trang chủ"""
    return render(request, 'accidents/index.html')

def add_accident(request):
    """Nhập thông tin vụ tai nạn"""
    if request.method == 'POST':
        form = AccidentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm vụ tai nạn thành công!')
            return redirect('add_accident')
    else:
        form = AccidentForm()
    
    return render(request, 'accidents/add_accident.html', {'form': form})

def map_view(request):
    """Hiển thị điểm tai nạn trên bản đồ"""
    accidents = Accident.objects.all()
    
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
            'district': acc.get_district_display(),
        })
    
    context = {
        'accidents_json': json.dumps(accidents_data),
    }
    return render(request, 'accidents/map.html', context)

from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Accident
from .forms import AccidentSearchForm

def search_accidents(request):
    form = AccidentSearchForm()
    results = None

    if request.method == 'POST':
        form = AccidentSearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Bao trùm toàn bộ ngày (00:00 - 23:59)
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())

            # Nếu muốn chắc chắn dùng timezone hiện tại (VN)
            start_datetime = timezone.make_aware(start_datetime)
            end_datetime = timezone.make_aware(end_datetime)

            results = Accident.objects.filter(datetime__range=[start_datetime, end_datetime])

    return render(request, 'accidents/search.html', {
        'form': form,
        'results': results
    })


def filter_accidents(request):
    """Lọc vụ tai nạn theo loại, mức độ, quận/huyện"""
    results = Accident.objects.all()
    form = FilterForm()

    total = results.count()
    xe_may_count = results.filter(accident_type='xe_may').count()
    o_to_count = results.filter(accident_type='o_to').count()
    rat_nang_count = results.filter(damage_level='rat_nang').count()
    
    if request.method == 'GET' and any(request.GET.values()):
        form = FilterForm(request.GET)
        if form.is_valid():
            # Áp dụng các bộ lọc
            if form.cleaned_data.get('accident_type'):
                results = results.filter(accident_type=form.cleaned_data['accident_type'])
            
            if form.cleaned_data.get('damage_level'):
                results = results.filter(damage_level=form.cleaned_data['damage_level'])
            
            if form.cleaned_data.get('district'):
                results = results.filter(district=form.cleaned_data['district'])
                
    
    context = {
        'results': results,
        'total': total,
        'xe_may_count': xe_may_count,
        'o_to_count': o_to_count,
        'rat_nang_count': rat_nang_count,
    }
    return render(request, 'accidents/filter.html', context)

def statistics(request):
    """Thống kê số vụ tai nạn theo quận/huyện"""
    district_stats = Accident.objects.values('district').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Thêm tên hiển thị cho quận/huyện
    for item in district_stats:
        district_obj = dict(Accident.CANTHO_DISTRICTS)
        item['district_name'] = district_obj.get(item['district'], item['district'])
    
    districts = [item['district_name'] for item in district_stats]
    counts = [item['count'] for item in district_stats]
    
    context = {
        'district_stats': district_stats,
        'districts_json': json.dumps(districts),
        'counts_json': json.dumps(counts),
    }
    return render(request, 'accidents/statistics.html', context)

from django.shortcuts import render
from .models import Accident
from .forms import AccidentFilterForm

def filter_accidents(request):
    form = AccidentFilterForm(request.GET or None)
    accidents = Accident.objects.all()

    # Nếu có lọc thì áp dụng
    if form.is_valid():
        accident_type = form.cleaned_data.get('accident_type')
        damage_level = form.cleaned_data.get('damage_level')
        district = form.cleaned_data.get('district')

        if accident_type:
            accidents = accidents.filter(accident_type=accident_type)
        if damage_level:
            accidents = accidents.filter(damage_level=damage_level)
        if district:
            accidents = accidents.filter(district=district)

    # Thống kê nhanh
    total = accidents.count()
    xe_may_count = accidents.filter(accident_type='xe_may').count()
    o_to_count = accidents.filter(accident_type='o_to').count()
    rat_nang_count = accidents.filter(damage_level='rat_nang').count()

    context = {
        'form': form,
        'results': accidents,
        'total': total,
        'xe_may_count': xe_may_count,
        'o_to_count': o_to_count,
        'rat_nang_count': rat_nang_count,
    }
    return render(request, 'accidents/filter.html', context)
