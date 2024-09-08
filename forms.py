from django import forms
from .models import MarginCalculator

class MarginCalculatorForm(forms.ModelForm):
    # Поля для ввода вероятности исходов от пользователя
    home_team_probability = forms.FloatField(
        required=False,
        label='Вероятность победы домашней команды (%)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите вероятность в %'})
    )
    away_team_probability = forms.FloatField(
        required=False,
        label='Вероятность победы гостевой команды (%)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите вероятность в %'})
    )
    draw_probability = forms.FloatField(
        required=False,
        label='Вероятность ничьей (%)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите вероятность в % (если применимо)'})
    )

    class Meta:
        model = MarginCalculator
        fields = ['home_team_odds', 'away_team_odds', 'draw_odds']
        labels = {
            'home_team_odds': 'Коэффициент на домашнюю команду',
            'away_team_odds': 'Коэффициент на гостевую команду',
            'draw_odds': 'Коэффициент на ничью (если применимо)',
        }
        widgets = {
            'home_team_odds': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите коэффициент'}),
            'away_team_odds': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите коэффициент'}),
            'draw_odds': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите коэффициент (если применимо)'}),
        }

"""
Официальный сайт: https://kalkulator-marzhi.ru/
"""
