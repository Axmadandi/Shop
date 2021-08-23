from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
	path('', views.index, name="index"),
	path('card/', views.card, name="card"),
	path('checkout/', views.checkout, name="checkout"),
	path('main/', views.main, name="main"),
	path('detail/<pk>',views.ProductDetailView.as_view(),name='product_detail'),
	path('category/<slug:category_slug>', views.categoryDetail,name='category_detail'),
	path('tag/<slug:tag_slug>/', views.tagDetail,name='tag_detail'),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]