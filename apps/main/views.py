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
    df['shop_name'] = df['Website'].apply(lambda x: x.split('/')[2] if isinstance(x, str) and len(x.split('/')) > 2 else '')
    laptops = df.head(10).to_dict(orient='records')
    for laptop in laptops:
        if laptop['Discount'] > 0:
            laptop['Final_Price'] = laptop['Price'] - (laptop['Price'] * laptop['Discount'] / 100)
        else:
            laptop['Final_Price'] = laptop['Price']
    return render(request, 'index.html', {'laptops': laptops})



# Create your views here.
class Home(TemplateView):
    template_name = 'index.html'
