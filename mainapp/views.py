import datetime
import json
import os
import random

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from geekshop.settings import JSON_ROOT
from .models import Product, ProductCategory

#JSON_PATH = 'mainapp/json'

def load_from_json(file_name):
    with open(os.path.join(JSON_ROOT, file_name + '.json'), 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category_id=hot_product.category_id).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    _products = Product.objects.all()[:3]
    content = {
        'title': title,
        'products': _products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, page=1):
    print(pk)
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    #            sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))

    #basket = []
    #if request.user.is_authenticated:
    #    basket = Basket.objects.filter(user=request.user)
    # basket = get_basket(request.user)
    if pk is not None:
        if pk == 0:
            product_items = Product.objects.all().order_by('price')
            category = {
                'pk': 0,
                'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product_items = Product.objects.filter(category__pk=pk).order_by('price')

        items_on_page = request.session.get('items_on_page', 2)
        paginator = Paginator(product_items, items_on_page)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            # 'basket': basket,
        }
        return render(request, 'mainapp/products_list.html', content)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    # same_products = [
    #     {
    #         'name': 'стул 1',
    #         'desc': 'стул 1',
    #         'image_src': 'product-11.jpg',
    #         'alt': 'продукт 11'
    #     },
    #     {
    #         'name': 'стул 2',
    #         'desc': 'стул 2',
    #         'image_src': 'product-21.jpg',
    #         'alt': 'продукт 21'
    #     },
    #     {
    #         'name': 'стул 3',
    #         'desc': 'стул 3',
    #         'image_src': 'product-31.jpg',
    #         'alt': 'продукт 31'
    #     },
    # ]
    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
        # 'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    # JSON_ROOT = os.path.join(settings.BASE_DIR, 'mainapp/json/')
    # with open(os.path.join(JSON_ROOT, "contacts.json"), encoding='utf8') as json_file:
    #    locations = json.load(json_file)

    locations = load_from_json('contacts')

    content = {
        'title': title,
        'visit_date': visit_date,
        'locations': locations,
        # 'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contacts.html', content)


def not_found(request, exception):
    content = {
        'products': Product.objects.all()[:3]
    }
    return render(request, 'mainapp/custom_404.html', content)


def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    title = product_item.name
    content = {
        'product': product_item,
        # 'basket': get_basket(request.user),
        'links_menu': ProductCategory.objects.all(),
        'title': title,
        'same_products': get_same_products(product_item)
    }
    return render(request, 'mainapp/product.html', content)
