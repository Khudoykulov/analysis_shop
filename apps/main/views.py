import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.views.generic import TemplateView, CreateView
import csv
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.conf import settings


def index(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'laptop.csv')

    # CSV faylni Pandas bilan o'qish
    df = pd.read_csv(file_path, encoding='utf-8')

    # Ma'lumotlarni lug'at formatiga o‘tkazish
    df.rename(columns={'Image URL': 'Image_URL'}, inplace=True)
    df['shop_name'] = df['Website'].apply(
        lambda x: x.split('/')[2] if isinstance(x, str) and len(x.split('/')) > 2 else '')
    laptops = df.head(24).to_dict(orient='records')
    for laptop in laptops:
        if laptop['Discount'] > 0:
            laptop['Final_Price'] = laptop['Price'] - (laptop['Price'] * laptop['Discount'] / 100)
        else:
            laptop['Final_Price'] = laptop['Price']
        # Set up pagination (10 items per page)
    # paginator = Paginator(laptops, 10)  # 10 laptops per page
    # page_number = request.GET.get('page')  # Get the page number from the URL (e.g., ?page=2)
    # page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'laptops': laptops})


# Create your views here.
class Home(TemplateView):
    template_name = 'login.html'


from django.shortcuts import render
from datetime import datetime


def product_detail(request):
    product = {
        "name": "VASAGLE Storage Chest",
        "image_url": "https://via.placeholder.com/400",
        "asin": "B0BWYM5PQQ",
        "manufacturer": "VASAGLE",
        "model": "ULSB062T14",
        "category": "Furniture",
        "price": 65.99,
        "last_updated": datetime.now().strftime("%b %d, %Y %I:%M %p"),
        "amazon_url": "https://www.amazon.com/dp/B0BWYM5PQQ"
    }
    price_history = {
        "dates": ["2025-01-01", "2025-02-01", "2025-03-01"],
        "values": [75, 70, 65.99]
    }

    return render(request, 'product_detail.html', {
        "product": product,
        "price_dates": price_history["dates"],
        "price_values": price_history["values"]
    })

