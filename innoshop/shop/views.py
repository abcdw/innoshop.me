import json
from django.shortcuts import render
from .models import Category
from .models import Product
from django.http import HttpResponse
from .forms import OrderForm
from .forms import OrderForm, FeedbackForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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


# def order(request):
#     if request.method == 'POST':
#         esoatuhsoetu
#     request.session['products']
#     #  request.session['products'] = ['test product', 'another product']
#     #  request.session['products'].append(u'test')
#     #  request.session['products'].append(u'test')
#     #  request.session.modified = True

#     print request.session['products']
#     form = OrderForm()
#     print form.as_p()
#     return HttpResponse(form.as_p())


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


def get_products(request):
    counts = request.session.get('products', {})
    objs = Product.objects.filter(id__in=counts.keys()).values('id', 'name', 'price')
    products = map(lambda x: {'count': counts[str(x['id'])], 'product': x}, objs)
    return HttpResponse(json.dumps((products)))


def order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.create_order( request.session.setdefault('products', {}) )
            del request.session['products']
            request.session.modified = True
            return render(request, 'shop/thanks.html')

    form = OrderForm()
    context = {
        'form': form,
        'title': 'order form',
    }
    return render(request, 'shop/order.html', context)
    # return HttpResponse('cart')


def feedback(request):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.create_feedback()
    form = FeedbackForm()
    context = {
        'form': form,
        'title': 'feedback form',
    }
    return render(request, 'shop/feedback.html', context)
