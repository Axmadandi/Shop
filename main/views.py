from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
import json
import datetime
from django.views.generic import (
	DetailView,)
from django.contrib import messages
from .models import *
# Create your views here.

def index(request):
	categories = Category.objects.all()
	tags = Tag.objects.all()
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complate=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order,}

	products = Product.objects.all()

	context = {'products':products, 'cartItems':cartItems, 'categories':categories, 'tags':tags}
	return render(request, 'index.html', context)


def categoryDetail(request,category_slug):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complate=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order,}
	category = get_object_or_404(Category,slug=category_slug)
	products = Product.objects.filter(category=category)
	categories = Category.objects.all()
	context = {
		'products':products,
		'categories':categories,
		'cartItems':cartItems,
	}
	return render(request, 'category_detail.html', context)

def tagDetail(request,tag_slug):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complate=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order,}
	tag = get_object_or_404(Tag,slug=tag_slug)
	products = Product.objects.filter(tag=tag)
	categories = Category.objects.all()
	context = {
		'products':products,
		'cartItems':cartItems,
		'categories':categories
	}
	return render(request, 'category_detail.html', context)

def card(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complate=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'card.html', context)


def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complate=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)

def main(request):
	context = {}
	return render(request, 'main.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:',action)
	print('ProductID:',productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complate=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
		messages.success(request,'Maxsulot qabul qilindi')
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()


	return JsonResponse('Item was addeds', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == get_cart_total:
			order.complate = False
		order.save()

		if order.shipping == True:
			ShippingAdress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)

	else:
		print('User is not logget in ...')
	return JsonResponse('Payment complate', safe=False)



class ProductDetailView(DetailView):
	model = Product

def customHandler404(request, exception=None):
	return render(request, '404.html')