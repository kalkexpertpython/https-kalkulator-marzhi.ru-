from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import MarginCalculatorForm
from .models import CalculatorInfo, SiteSettings
from articles.models import Article
from authors.models import Author
from stats.tasks import save_usage_data
import datetime
from django.db.models import Count
from stats.models import UsageStats
from django.utils import timezone

def calculate_margin_view(request):
    result = None
    product_margin = None
    current_year = datetime.datetime.now().year
    infos = CalculatorInfo.objects.all()
    settings = SiteSettings.objects.first()

    form = MarginCalculatorForm()

    # Получаем последние статьи и авторов
    latest_articles = Article.objects.order_by('-created_at')[:3]
    authors = Author.objects.all()[:3]

    # Собираем данные по использованию калькулятора
    today = timezone.now().date()  # Текущая дата
    stats_today = UsageStats.objects.filter(used_at__date=today).count()
    top_cities = UsageStats.objects.values('city').annotate(count=Count('city')).order_by('-count')[:5]
    last_usage = UsageStats.objects.latest('used_at')

    if request.method == 'POST':
        # Сбор IP-адреса пользователя
        user_ip = get_client_ip(request)
        save_usage_data.delay(user_ip)

        # Обработка формы для букмекерской маржи
        if 'home_team_odds' in request.POST:
            form = MarginCalculatorForm(request.POST)
            if form.is_valid():
                margin_calculator = form.save(commit=False)
                margin = margin_calculator.calculate_margin()
                home_prob, away_prob, draw_prob = margin_calculator.calculate_probabilities()
                real_home_odds, real_away_odds, real_draw_odds = margin_calculator.calculate_real_odds()

                result = {
                    'margin': margin,
                    'home_prob': home_prob,
                    'away_prob': away_prob,
                    'draw_prob': draw_prob,
                    'real_home_odds': real_home_odds,
                    'real_away_odds': real_away_odds,
                    'real_draw_odds': real_draw_odds,
                }

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse(result)

        elif 'cost_price' in request.POST:
            cost_price = float(request.POST.get('cost_price'))
            sale_price = float(request.POST.get('sale_price'))
            if sale_price > 0:
                product_margin = round((sale_price - cost_price) / sale_price * 100, 2)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'product_margin': product_margin})

    return render(request, 'calculator/calculate_margin.html', {
        'form': form,
        'result': result,
        'product_margin': product_margin,
        'current_year': current_year,
        'infos': infos,
        'site_settings': settings,
        'latest_articles': latest_articles,
        'authors': authors,
        'stats_today': stats_today,
        'top_cities': top_cities,
        'last_usage': last_usage,
        'today': today,  # Передаем текущую дату
    })

Официальный сайт: https://kalkulator-marzhi.ru/
