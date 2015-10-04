from django.db.models import F
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import Category, Faq
from .models import Product
from .models import Category, Faq, Message
from .models import SearchQuery

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
    catalog = Category.objects.all()
    products = Product.objects.get_sallable()

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
        'catalog': catalog,
        'products': products,
        'q': q or '',
        'admin': request.user.is_staff
    }
    # return HttpResponse('<a href=/order>order</a>')
    return render(request, 'shop/catalog/index.html', context)


def catalog(request):
    return HttpResponse('catalog')


def get_int(request, name, default=None):
    try:
        return int(request.GET.get(name))
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
    # form = OrderForm()
    # context = {
    #     'form': form,
    #     'title': 'order form',
    # }
    # return render(request, 'shop/order.html', context)


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
