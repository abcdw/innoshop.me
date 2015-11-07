# encoding: utf-8

from django.db.models import Q
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import xlsxwriter
from shop.models import Order

__author__ = 'kittn'


def expeditor_view(request):
	# collecting new/active orders
	orders = Order.objects\
		.filter(Q(status='new') | Q(status='active'))\
		.all()\
		.order_by('status')\
		.reverse()

	products = list()
	excel = xlsxwriter.Workbook("tmp.xlsx")
	page = excel.add_worksheet("Products")
	row = 1
	# printing table header
	header = [
		u"SKU", u"Категория", u"Название", u"Цена",
		u"Закупочная цена", u"Количество", u"Изображение"
	]
	for _ in range(0, len(header)):
		page.set_column(0, _, len(header[_]))
		page.write(0, _, header[_])

	for order in orders:  # now building list of ProductItems from each Order
		for product in order.get_items().all():
			# grouping categories to sort on them later
			product.categories = " -> ".join(sorted([cat.name for cat in product.product.categories.all()]))
			products.append(product)

	# sorting products
	products.sort(key=lambda prod: prod.categories)

	# i know, we can do it in the loop above, but this loop is for readability
	# generating xlsx from data
	for product in products:
		product_row = [
			product.SKU, product.categories, product.name, product.actual_price,
			product.actual_price, product.count * product.min_count, product.img_url
		]
		for _ in range(0, len(product_row)):
			page.write(row, _, product_row[_])

		row += 1

	excel.close()

	# generating link to download xlsx
	response = FileResponse(open('tmp.xlsx', "rb"))
	response['Content-Disposition'] = 'attachment; filename=expeditor_products.xlsx'

	return response


def reports_page_view(request):
	return render(request, "reports/reports_page.html")


def supplier_view(request):
	return HttpResponse("Error: not implemented!")
