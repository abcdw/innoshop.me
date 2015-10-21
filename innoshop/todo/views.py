from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from shop.models import Category, Faq
from shop.models import Product
from shop.models import ProductItem
from shop.models import Order


import json
import inspect
import datetime
import hashlib

from django.contrib.admin.views.decorators import staff_member_required
from shop.views import degrades

@staff_member_required
def admin_dashboard(request):
    context = {
        'cnt_new': Order.objects.filter(status='new').count(),
        'cnt_active': Order.objects.filter(status='active').count(),
        'orders': Order.objects.filter(Q(status='new') | Q(status='active')).all().order_by('status').reverse()
    }
    return render(request, 'todo/dashboard.html', context)


@staff_member_required
def admin_todo_list(request):
    active = Order.objects.filter(status='active').all()
    id = 1
    products = []
    for t_order in active:
        for t_product in t_order.get_items().all():
            t_product.category = ""
            for t_cat in t_product.product.categories.all():
                t_product.category += t_cat.name + '->'
            t_product.category = t_product.category[:-2]
            t_product.currentId = id
            id += 1
            products.append(t_product)
    products.sort(key=lambda x: x.category)
    context = {
        'products': products
    }
    return render(request, 'todo/todo_list.html', context)

@staff_member_required
def admin_todo_list_print(request):
    active = Order.objects.filter(status='active').all()
    id = 1
    products = []
    for t_order in active:
        for t_product in t_order.get_items().all():
            t_product.category = ""
            for t_cat in t_product.product.categories.all():
                t_product.category += t_cat.name + '->'
            t_product.category = t_product.category[:-2]
            t_product.currentId = id
            id += 1
            products.append(t_product)
    products.sort(key=lambda x: x.category)
    context = {
        'products': products
    }
    return render(request, 'todo/todo_list_print.html', context)

@staff_member_required
def admin_view_order(request):
    t_order = Order.objects.get(pk=request.GET.get("pk"))
    products = []
    price = 0.0
    for t_product in t_order.get_items().all():
        products.append(t_product)
        price += t_product.price
    if t_order.contact[0] =='@':
            t_order.contact = t_order.contact[1:]
            t_order.save()
    context = {
        'date' : t_order.create_time.strftime("%d/%m/%Y"),
        'order': t_order,
        'products': products,
        'price': price,
        'ship_price': price * 0.05,
        'total': price * 1.05
    }
    return render(request, 'todo/view_order.html', context)


@staff_member_required
def get_order_hash(request):
    try:
        order = Order.objects.get(pk=request.GET.get("pk"))
        response = HttpResponse()
        response['Content-Type'] = 'application/json'
        md = hashlib.md5()
        md.update(str(order.pk) + "@" + order.contact + "@" + order.create_time.__str__())
        order.order_hash = md.hexdigest()
        order.save()
        result = {'error': 0,
                  'hash': order.order_hash}
        response.content = json.dumps(result)
        return response
    except Exception, e:
        return HttpResponse({'error': e.message})

@staff_member_required
def set_order_status(request):
    try:
        order = Order.objects.get(pk=request.GET.get("pk"))
        response = HttpResponse()
        response['Content-Type'] = 'application/json'
        order.status = request.GET.get("status")
        md = hashlib.md5()
        md.update(str(order.pk) + "@" + order.contact + "@" + order.create_time.__str__())
        order.order_hash = md.hexdigest()
        order.save()
        result={'error':0,
                'hash': order.order_hash}
        response.content = json.dumps(result)
        return response
    except Exception, e:
        return HttpResponse(json.dumps({'error':e.message}))

@degrades
def view_order(request):
    try:
        order = Order.objects.get(order_hash=request.GET.get("hash"))
        products = []
        price = 0.0
        for t_product in order.get_items().all():
            products.append(t_product)
            price += t_product.price
        if order.contact[0] =='@':
            order.contact = order.contact[1:]
            order.save()
        context = {
            'order': order,
            'products': products,
            'price': price,
            'ship_price': price * 0.05,
            'total': price * 1.05,
            'date': order.create_time.strftime('%m/%d/%Y'),
            'admin': request.user.is_staff
        }
        return render(request, 'todo/user_view_order.html', context)
    except Exception, e:
        return HttpResponse(json.dumps({'error': e.message}))