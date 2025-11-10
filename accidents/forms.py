from django import forms
from .models import Accident

class AccidentForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields = ['location', 'latitude', 'longitude', 'accident_type', 
                  'datetime', 'damage_level', 'district']
        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ví dụ: Cầu Cần Thơ, Chợ Cái Răng'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Ví dụ: 10.0452'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Ví dụ: 105.7469'
            }),
            'accident_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'datetime': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'damage_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'district': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class SearchForm(forms.Form):
    start_date = forms.DateTimeField(
        label='Từ ngày',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )
    end_date = forms.DateTimeField(
        label='Đến ngày',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=True
    )

class FilterForm(forms.Form):
    accident_type = forms.ChoiceField(
        label='Loại tai nạn',
        choices=[('', 'Tất cả')] + Accident.ACCIDENT_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )
    damage_level = forms.ChoiceField(
        label='Mức độ thiệt hại',
        choices=[('', 'Tất cả')] + Accident.DAMAGE_LEVELS,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )
    district = forms.ChoiceField(
        label='Quận/Huyện',
        choices=[('', 'Tất cả')] + Accident.CANTHO_DISTRICTS,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )

class AccidentFilterForm(forms.Form):
    accident_type = forms.ChoiceField(
        choices=[('', '--- Tất cả loại tai nạn ---')] + Accident.ACCIDENT_TYPES,
        required=False,
        label='Loại tai nạn',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    damage_level = forms.ChoiceField(
        choices=[('', '--- Tất cả mức độ ---')] + Accident.DAMAGE_LEVELS,
        required=False,
        label='Mức độ thiệt hại',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    district = forms.ChoiceField(
        choices=[('', '--- Tất cả quận/huyện ---')] + Accident.CANTHO_DISTRICTS,
        required=False,
        label='Quận/Huyện',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class AccidentSearchForm(forms.Form):
    start_date = forms.DateField(
        label="Từ ngày",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    end_date = forms.DateField(
        label="Đến ngày",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )