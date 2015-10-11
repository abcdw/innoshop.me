from django.db.models import F
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.core import serializers
from django.conf import settings

from .models import Category, Faq
from .models import Product
from .models import Category, Faq, Message
from .models import SearchQuery
from .models import Order

from .forms import OrderForm
from .forms import OrderForm, FeedbackForm

import json
import inspect
import datetime

from django.contrib.admin.views.decorators import staff_member_required


def degrades(function):
    def wrap(request, *args, **kwargs):
        if function.__name__ in settings.DEGRADE:
            # better because it's not necessary to redirect
            return HttpResponse('Yep, we know. We are working on that =)', status=503)
            #  return HttpResponseRedirect(reverse('maintenance'))
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


@degrades
def index(request):
    catalog = Category.objects.filter(product_count__gt=0)
    category = None

    def find_children(src, dst, id):
        for item in src:
            if item['parent_id'] == id:
                out = {'item': item, 'children': []}
                dst.append(out)
                src.remove(item)
                find_children(src, out['children'], item['id'])

    catalog_tree = []
    catalog_list = list(catalog.values('name', 'id', 'parent_id', 'product_count'))
    for item in catalog_list:
        if item['parent_id'] is None:
            out = {'item': item, 'children': []}
            catalog_tree.append(out)
            catalog_list.remove(item)
            find_children(catalog_list, out['children'], item['id'])

    products = Product.objects.get_sallable()

    cat = get_int(request, 'c')
    if cat:
        category = Category.objects.get(id=cat)
        products = products.filter(categories__id__contains=cat)

    q = request.GET.get('q')
    if q:
        products = Product.objects.smart_filter(q)
        SearchQuery.add_query(q, products.count())

    paginator = Paginator(products, settings.PRODUCTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'catalog': catalog_tree,
        'products': products,
        'q': q or '',
        'cat': cat or '',
        'category': category or '',
        'admin': request.user.is_staff
    }

    return render(request, 'shop/catalog/index.html', context)


def catalog(request):
    return HttpResponse('catalog')


def get_int(request, name, default=None):
    try:
        return int(request.GET.get(name) or '')
    except ValueError:
        return default


@degrades
def add_product(request):
    result = {'status': 'error', 'result': 'use GET method'}
    if request.method == 'GET':
        try:
            id = get_int(request, 'id')
            count = get_int(request, 'count', 0)
            if id >= 0 and count:
                id = str(id)
                s = request.session.setdefault('products', {})
                s[id] = s.get(id, 0) + count
                if s[id] <= 0:
                    del s[id]
                request.session.modified = True
                result.update({'status': 'ok', 'result': s.get(id)})
        except Exception, e:
            result.update({'result': 'invalid id or count'})
    return HttpResponse(json.dumps(result))


@degrades
def get_products(request):
    counts = request.session.get('products', {})
    objs = Product.objects.filter(id__in=counts.keys()).values('id', 'name', 'price', 'min_count')
    products = map(lambda x: {'count': counts[str(x['id'])], 'product': x}, objs)
    return HttpResponse(json.dumps((products)))


@degrades
def order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.create_order(request.session.setdefault('products', {}))
            del request.session['products']
            request.session.modified = True
            return render(request, 'shop/thanks.html')

    raise Http404


@degrades
def feedback(request):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.create_feedback()
    form = FeedbackForm()
    try:
        faq = Faq.objects.get(name='FAQ')
    except Exception, e:
        faq = False
    context = {
        'form': form,
        #  'title': 'feedback form',
        'faq': faq
    }
    return render(request, 'shop/feedback.html', context)


def get_messages(request):
    messages = Message.objects.filter(start__lte=datetime.date.today(),
                                      end__gte=datetime.date.today()).values('name', '_text_rendered')
    return HttpResponse(json.dumps(list(messages)))


@staff_member_required
def update_rating(request):
    result = {'status': 'error', 'result': 'use GET method'}
    if request.method == 'GET':
        try:
            id = get_int(request, 'id')
            count = get_int(request, 'count', 0)
            if id >= 0 and count:
                product = Product.objects.filter(id=id)
                product.update(rating=F('rating') + count)
                result.update({'status': 'ok', 'result': product.first().rating})
        except Exception, e:
            result.update({'result': 'invalid id or count'})
    return HttpResponse(json.dumps(result))


@staff_member_required
def get_orders(request):
    result = Order.objects.filter(status='active')
    return HttpResponse(serializers.serialize("json", result))


@staff_member_required
def get_order_products(request):
    result = Order.objects.filter(pk=request.GET.get("pk"))[0].get_items().all()
    return HttpResponse(serializers.serialize("json", result))
