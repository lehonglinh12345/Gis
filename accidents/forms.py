# accidents/forms.py
from django import forms
from .models import Accident

class AccidentForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields = ['location', 'latitude', 'longitude', 'accident_type', 
                  'datetime', 'damage_level', 'commune_code']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Cầu Rồng, Đà Nẵng'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'accident_type': forms.Select(attrs={'class': 'form-control'}),
            'datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'damage_level': forms.Select(attrs={'class': 'form-control'}),
            'commune_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ví dụ: 81519002',
                'readonly': 'readonly'
            }),
        }

class AccidentFilterForm(forms.Form):
    accident_type = forms.ChoiceField(
        choices=[('', '--- Tất cả loại tai nạn ---')] + Accident.ACCIDENT_TYPES,
        required=False, label='Loại tai nạn',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    damage_level = forms.ChoiceField(
        choices=[('', '--- Tất cả mức độ ---')] + Accident.DAMAGE_LEVELS,
        required=False, label='Mức độ thiệt hại',
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