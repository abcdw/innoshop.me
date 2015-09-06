from django.shortcuts import render
from .models import Category
from django.http import HttpResponse
from .forms import OrderForm


def index(request):
    catalog = Category.objects.all()
    context = {
        'catalog': catalog,
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
            id = request.GET.get('id', None)
            count = int(request.GET.get('count', 0))
            if id:
                if not request.session.has_key('products'):
                    request.session['products'] = {}

                if not type(request.session['products']) is dict:
                    request.session['products'] = {}
                s = request.session['products']

                if s.has_key(id):
                    s[id] += count
                else:
                    s[id] = count

                if s[id] < 0:
                    s[id] = 0

                request.session.modified = True
            return HttpResponse('added {} items of product {}, current count: {}'.format(count, id, s[id]))
        except Exception, e:
            return HttpResponse('provide int id and count in GET')

    return HttpResponse('provide int id and count in GET')


def get_products(request):
    return HttpResponse('get_products')


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



