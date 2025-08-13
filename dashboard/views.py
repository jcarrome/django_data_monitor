# dashboard/views.py
from django.shortcuts import render
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from collections import Counter
from datetime import datetime

# Vista para renderizar la plantilla 'index.html'
@login_required
def index(request):
    response = requests.get(settings.API_URL)
    posts = response.json()

    product_counter = Counter()
    product_dates = {}

    for post in posts.values():
        for key, value in post.items():
            if key.startswith('product'):
                product_name = str(value)
                product_counter[product_name] += 1
                timestamp = post.get('timestamp')
                if timestamp:
                    timestamp = timestamp.replace('a. m.', 'AM').replace('p. m.', 'PM')
                    try:
                        dt = datetime.strptime(timestamp, "%d/%m/%Y, %I:%M:%S %p")
                        if product_name not in product_dates or dt > product_dates[product_name]:
                            product_dates[product_name] = dt
                    except ValueError:
                        continue

    total_products = len(product_counter)
    most_requested = product_counter.most_common(1)[0][0] if product_counter else None
    least_requested = product_counter.most_common()[-1][0] if product_counter else None
    newest_product = max(product_dates, key=product_dates.get) if product_dates else None

    products_table = [{'name': k, 'count': v} for k, v in product_counter.items()]

    # Agrupar por fecha y contar productos por fecha
    date_counts = {}
    for post in posts.values():
        timestamp = post.get('timestamp')
        if timestamp:
            timestamp = timestamp.replace('a. m.', 'AM').replace('p. m.', 'PM')
            try:
                dt = datetime.strptime(timestamp, "%d/%m/%Y, %I:%M:%S %p")
                date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                # Contar cuántos productos hay en este post
                product_count = sum(1 for key in post if key.startswith('product'))
                if date_str not in date_counts:
                    date_counts[date_str] = 0
                date_counts[date_str] += product_count
            except ValueError:
                continue

    # timeline_data para la gráfica
    timeline_data = [
        {'date': date, 'count': count}
        for date, count in sorted(date_counts.items())
    ]

    data = {
        'title': "Dashboard",
        'total_responses': len(posts),
        'total_products': total_products,
        'most_requested': most_requested,
        'least_requested': least_requested,
        'newest_product': newest_product,
        'products_table': products_table,
        'timeline_data': timeline_data,
    }

    return render(request, 'dashboard/index.html', data)
