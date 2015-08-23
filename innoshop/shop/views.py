from django.shortcuts import render
from .models import Category


def index(request):
    catalog = Category.objects.all()
    context = {
        'catalog': catalog
    }
    return render(request, 'shop/index.html', context)
