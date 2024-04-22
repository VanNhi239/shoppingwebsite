from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('detail/', views.detail, name="detail"),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name="checkout"),
    # path('update_item/', views.updateItem, name="update_item"),
    path('login/', views.login_user, name="login"),
	path('logout/', views.logout_user, name="logout"),
	path('register/', views.register_user, name="register"),
]