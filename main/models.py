from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
	name = models.CharField('Nomi',max_length=150,)
	slug = models.SlugField('*',max_length=150, unique=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('main:category_detail', kwargs={'category_slug':self.slug})


class Tag(models.Model):
	name = models.CharField('Nomi',max_length=150,)
	slug = models.SlugField('*',max_length=150, unique=True)
	image = models.ImageField(upload_to='product_images/')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('main:tag_detail', kwargs={'tag_slug':self.slug})


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField('Ismi',max_length=200, null=True)
	email = models.CharField('Email',max_length=200, null=True)


	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField('nomi',max_length=200, null=True)
	price = models.FloatField()
	category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='categoriys')
	tag = models.ForeignKey(Tag,on_delete=models.CASCADE,related_name='tags')
	image = models.ImageField(upload_to='product_images/')
	digital = models.BooleanField(default=False, null=True, blank=False)
	data = models.PositiveIntegerField('Ishlab chiqilgan yili')
	m_type = models.CharField('Turi', max_length=500)
	
	def __str__(self):
		return self.name


	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
	data_orderd = models.DateTimeField(auto_now_add=True)
	complate = models.BooleanField(default=False, null=True	, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	data_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=500, null=False)
	state = models.CharField(max_length=500, null=False)
	zipcode = models.CharField(max_length=500, null=False)
	data_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address