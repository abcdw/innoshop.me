import json
from django.shortcuts import render
from .models import Category
from .models import Product
from django.http import HttpResponse
from .forms import OrderForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    catalog = Category.objects.all()
    products = Product.objects.get_sallable()

    q = request.GET.get('q')
    if q:
        products = products.filter( name__icontains = q )

    paginator = Paginator(products, 25)
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
    if request.method == 'GET':
        try:
            id = safe_cast(request.GET.get('id'), int, None)
            count = int(request.GET.get('count', 0))
            if id >= 0:
                id = str(id)
                if not request.session.has_key('products'):
                    request.session['products'] = {}

                if not type(request.session['products']) is dict:
                    request.session['products'] = {}
                s = request.session['products']

                if s.has_key(id):
                    s[id] += count
                else:
                    s[id] = count

                if s[id] <= 0:
                    del s[id]

                if s.has_key(id):
                    cur_count = s[id]
                else:
                    cur_count = 0
                request.session.modified = True
                return HttpResponse('added {} items of product {}, current count: {}'.format(count, id, cur_count ))
        except Exception, e:
            return HttpResponse('provide int id and count in GET')

    return HttpResponse('provide int id and count in GET')


def get_products(request):
    counts = {}
    if request.session.has_key('products'):
        counts = request.session['products']
    objs = Product.objects.filter(id__in=counts.keys()).values('id', 'name', 'price')
    products = {}
    for p in objs:
        products[str(p['id'])] = { 'count': counts[str(p['id'])], 'product': p }
    return HttpResponse(json.dumps((products)))


def order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.create_order()

    form = OrderForm()
    context = {
        'form': form,
        'title': 'order form',
    }
    return render(request, 'shop/order.html', context)
    # return HttpResponse('cart')


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except ValueError:
        return default
