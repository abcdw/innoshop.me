# encoding: utf-8
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import time
import xlsxwriter
import os
from shop.models import Order, SubOrder

__author__ = 'kittn'


@staff_member_required
def expeditor_view(request):
	orders = Order.objects\
		.filter(Q(status='new') | Q(status='active'))\
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
		for product in order.productitem_set.all():
			# grouping categories to sort on them later
			product.categories = " -> ".join(sorted([cat.name for cat in product.product.categories.all()]))
			products.append(product)

	products.sort(key=lambda prod: prod.categories)

	# i know, we can do it in the loop above, but this loop is for readability
	# generating xlsx from data
	for product in products:
		product_row = [
			product.SKU, product.categories, product.name, product.actual_price,
			product.actual_price, product.count * product.min_count, product.img_url
		]
		page.write_url(row, 0, product.source_link, string=product.SKU)
		for _ in range(1, len(product_row)):
			page.write(row, _, product_row[_])

		row += 1

	excel.close()

	# generating link to download xlsx
	date = time.strftime("%d.%m.%y", time.localtime())
	response = FileResponse(open('tmp.xlsx', "rb"))
	response['Content-Disposition'] = 'attachment; filename=expeditor_%s.xlsx' % date

	os.remove("tmp.xlsx")

	return response


@staff_member_required
def reports_page_view(request):
	# gathering new orders from Metro
	suborders = SubOrder.objects.filter(Q(status="new") | Q(status="active"))
	suborders = filter(lambda x: unicode(x) == u"Metro", suborders)

	for suborder in suborders:
		suborder.admin_url = "/admin/shop/order/%d" % suborder.order.id
		suborder.report_url = "/report/id/%d" % suborder.id
		suborder.contact = suborder.order.contact

	return render(request, "reports/reports_page.html", {"orders_info": suborders})


def generate_user_page(suborder, page, fmt):

	# generating header of the page
	page.merge_range('B1:F1', u"Бланк заявки и приема товара c магазина Метро в г.Иннополис", fmt)
	page.set_column('B:C', 50)
	page.set_column('F:F', 15)
	headers = [
		u"Номер заказа", u"Дата заявки", u"Дата доставки", u"Адрес доставки",
		u"Время доставки (предпочитаемое)", u"Фамилия Имя и телефон клиента",
		u"Форма оплаты"
	]
	values = [
		str(suborder.id), suborder.order.create_time.strftime("%d.%m.%y, %H:%M"),
		time.strftime("%d.%m.%y", time.localtime()), "_" * 5, "_" * 5, suborder.order.contact, "_" * 5
	]
	for i in range(len(headers)):
		page.write_string(i + 2, 1, headers[i], fmt)
		page.write_string(i + 2, 2, values[i])

	# now generating list of items in order
	row = 4 + len(headers)
	total_value = 0

	product_info = [
		u"#", u"Наименование товара полное", u"Aртикул", u"ед.изм.", u"кол-во", u"цена", u"сумма"
	]
	page.write_row(row - 1, 0, product_info, fmt)

	for product in suborder.get_items().all():
		product_data = [
			row - 10, product.name, product.SKU, u"value",
			product.count, product.actual_price, product.count * product.actual_price
		]
		total_value += product.count * product.actual_price
		page.write_row(row, 0, product_data)
		row += 1

	row += 2

	# now footer left
	footers = [
		u"Итого:", u"Комиссия 15%:", u"Всего:", u"Депозит", u"Заказ", u"Остаток депозита"
	]
	footers_data = [
		total_value, total_value * 0.15, total_value * 1.15, 0, total_value * 1.15, 0
	]

	for _ in range(len(footers)):
		page.merge_range("E%d:F%d" % (row + _, row + _), footers[_], fmt)
		page.write_number("G%d" % (row + _), footers_data[_])

	row += len(footers) + 1

	last_notes = [
		u"Сдал продукцию (представитель Трапезы Ф.И., подпись):",
		u"Принял продукцию (клиент Ф.И., подпись):",
		u"Как вы оцените работу ООО Трапезы по доставке по пяти бальной шкале:"
	]
	for _ in range(len(last_notes)):
		page.merge_range("B%d:D%d" % (row, row), last_notes[_], fmt)
		page.merge_range("E%d:G%d" % (row, row), "_" * 20)
		row += 2


def generate_file_response(filename, output_name):
	date = time.strftime("%d.%m.%y", time.localtime())
	response = FileResponse(open(filename, "rb"))
	response['Content-Disposition'] = 'attachment; filename=%s_%s.xlsx' % (output_name, date)

	return response


@staff_member_required
def reports_user_view(request):
	suborders = SubOrder.objects.filter(Q(status="new") | Q(status="active"))

	# i can put expression above as a parameter to 'filter', but it won't be readable
	suborders = filter(lambda x: unicode(x) == u"Metro", suborders)
	print suborders

	report = xlsxwriter.Workbook("tmp.xlsx")
	bold = report.add_format({'bold': 1})
	names = {}

	for suborder in suborders:
		username = suborder.order.contact
		# avoiding same pages name error for the same user
		sheet_num = names.setdefault(username, 0)
		names[username] += 1

		generate_user_page(suborder, report.add_worksheet(username + str(sheet_num)), bold)
	report.close()

	# generating link to download xlsx
	response = generate_file_response('tmp.xlsx', "users")

	os.remove("tmp.xlsx")

	return response


def report_order_id(request, order_id):
	excel = xlsxwriter.Workbook("tmp.xlsx")
	bold = excel.add_format({'bold': 1})
	suborder = filter(lambda x: x.id == int(order_id), SubOrder.objects.all())[0]

	generate_user_page(suborder, excel.add_worksheet(str(order_id)), bold)
	excel.close()

	response = generate_file_response("tmp.xlsx", str(order_id))
	os.remove("tmp.xlsx")

	return response
