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
    file_path = os.path.join(settings.BASE_DIR, 'data', 'data.csv')

    # CSV faylni Pandas bilan o'qish
    df = pd.read_csv(file_path, encoding='utf-8')

    # Ma'lumotlarni lug'at formatiga o‘tkazish
    df.rename(columns={'Image URL': 'Image_URL'}, inplace=True)
    df['shop_name'] = df['Website'].apply(
        lambda x: x.split('/')[2] if isinstance(x, str) and len(x.split('/')) > 2 else '')
    laptops = df.to_dict(orient='records')
    for laptop in laptops:
        if laptop['Discount'] > 0:
            laptop['Final_Price'] = laptop['Price'] - (laptop['Price'] * laptop['Discount'] / 100)
        else:
            laptop['Final_Price'] = laptop['Price']
            # Qidiruv so‘rovini olish
    search_query = request.GET.get('search', '').strip().lower()
    selected_category = request.GET.get('category', 'All Categories')

    # Qidiruv bo‘yicha filtr
    filtered_laptops = laptops
    if search_query:
        filtered_laptops = [
            laptop for laptop in laptops
            if (search_query in laptop['Name'].lower() or
                search_query in str(laptop.get('Category', '')).lower())
        ]

    # Category bo‘yicha filtr
    if selected_category != 'All Categories':
        filtered_laptops = [
            laptop for laptop in filtered_laptops
            if str(laptop.get('Category', '')) == selected_category
        ]
    filtered_laptops = sorted(filtered_laptops, key=lambda x: x['Final_Price'], reverse=False)
    # Pagination
    paginator = Paginator(filtered_laptops, 8)  # Har sahifada 8 ta mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Kategoriyalarni olish (dropdown uchun)
    categories = list(set(laptop.get('Category', '') for laptop in laptops))
    categories = ['All Categories'] + sorted(categories)

    return render(request, 'index.html', {
        'laptops': page_obj.object_list,
        'paginator': paginator,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query
    })


# Create your views here.
class Home(TemplateView):
    template_name = 'login.html'


def product_detail(request, pk):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'data.csv')

    # CSV faylni Pandas bilan o'qish
    df = pd.read_csv(file_path, encoding='utf-8')

    # DataFrame'dan berilgan pk (ID) ga mos keladigan qatorni topish
    try:
        # Agar CSV faylda 'id' ustuni bo'lsa va pk int sifatida kelayotgan bo'lsa
        object_data = df[df['id'] == int(pk)].iloc[0].to_dict()
        object_data['shop_name'] = (
            object_data['Website'].split('/')[2]
            if isinstance(object_data['Website'], str) and len(object_data['Website'].split('/')) > 2
            else ''
        )
        original_price = object_data['Price']
        discount = object_data['Discount']  # Chegirma foizi (masalan, 66.67)
        discounted_price = original_price * (1 - discount / 100)  # Chegirmadan keyingi narx
        object_data['discounted_price'] = discounted_price  # Yangi narxni qo'shamiz

        # Joriy mahsulotning kategoriyasiga mos boshqa 5 ta mahsulotni tanlash
        category = object_data.get('Category')
        if category:
            # Joriy mahsulotni (id == pk) chiqarib tashlab, shu kategoriyadagi boshqa mahsulotlarni olish
            highlighted_products = df[
                (df['Category'] == category) & (df['id'] != int(pk))
                ].head(5).to_dict('records')  # 5 ta mahsulot
            # Har bir mahsulot uchun o'rtacha narxni hisoblash (masalan)
            for product in highlighted_products:
                product['Avg_Price'] = product['Price'] * 1.3  # O'rtacha narx (masalan)
        else:
            highlighted_products = []  # Agar kategoriya bo'lmasa, bo'sh ro'yxat
    except (IndexError, KeyError, ValueError):
        return render(request, '404.html', {'error': 'Product not found'})

    context = {
        'object': object_data,
        'related_products': highlighted_products  # Bog'liq mahsulotlarni qo'shamiz
    }
    return render(request, 'product_detail.html', context)
