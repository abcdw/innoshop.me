from django.http import HttpResponse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import Category, Faq
from .models import Product
from .forms import OrderForm
from .forms import OrderForm, FeedbackForm

import json
import inspect


def degrades(function):
    def wrap(request, *args, **kwargs):
        if function.__name__ in settings.DEGRADE:
            # better because it's not necessary to redirect
            return HttpResponse('Yep, we know. We are working on that =)')
            #  return HttpResponseRedirect(reverse('maintenance'))
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


@degrades
def index(request):
    catalog = Category.objects.all()
    products = Product.objects.get_sallable()

    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)

    paginator = Paginator(products, 12)
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
        'catalog': catalog,
        'products': products,
        'q': q or ''
    }
    # return HttpResponse('<a href=/order>order</a>')
    return render(request, 'shop/catalog/index.html', context)


def catalog(request):
    return HttpResponse('catalog')


@degrades
def add_product(request):
    def get_int(name, default=None):
        try:
            return int(request.GET.get(name))
        except ValueError:
            return default

    result = {'status': 'error', 'result': 'use GET method'}
    if request.method == 'GET':
        try:
            id = get_int('id')
            count = get_int('count', 0)
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
            order_form.create_order( request.session.setdefault('products', {}) )
            del request.session['products']
            request.session.modified = True
            return render(request, 'shop/thanks.html')

    raise Http404
    form = OrderForm()
    context = {
        'form': form,
        'title': 'order form',
    }
    return render(request, 'shop/order.html', context)


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
        'title': 'feedback form',
        'faq': faq
    }
    return render(request, 'shop/feedback.html', context)
