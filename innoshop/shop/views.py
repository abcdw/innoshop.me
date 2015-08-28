from django.shortcuts import render
from .models import Category
from django.http import HttpResponse
from .forms import OrderForm


def index(request):
    catalog = Category.objects.all()
    context = {
        'catalog': catalog
    }
    return HttpResponse('<a href=/order>order</a>')
    return render(request, 'shop/index.html', context)


def catalog(request):
    return HttpResponse('catalog')


def order(request):
    if request.method == 'POST':
        esoatuhsoetu
    request.session['products']
    #  request.session['products'] = ['test product', 'another product']
    #  request.session['products'].append(u'test')
    #  request.session['products'].append(u'test')
    #  request.session.modified = True

    print request.session['products']
    form = OrderForm()
    print form.as_p()
    return HttpResponse(form.as_p())


def add_product(request):
    return HttpResponse('add_product')


def get_products(request):
    return HttpResponse('get_products')


def cart(request):
    return HttpResponse('cart')



