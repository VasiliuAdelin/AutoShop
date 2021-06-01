"""icapitstop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login.html',views.login, name='login'),
    path('admin.html',views.adminPage, name='adminPage'),
    path('index.html',views.index, name='index'),
    path('account.html',views.account, name='account'),
    path('shop.html',views.shopShowAllProducts, name='shopShowAllProducts'),
    path('shopShowAllProducts',views.shopShowAllProducts, name='shopShowAllProducts'),
    path('cart.html',views.displayCartProducts, name='displayCartProducts'),
    path('place_order',views.place_order, name='place_order'),
    path('checkout.html',views.checkout, name='checkout'),
    path('supplier-orders.html',views.supplierPage, name='supplierPage'),
    path('supplier-products.html',views.supplierPageProducts, name='supplierPageProducts'),
    path('modifyOrderState',views.modifyOrderState, name='modifyOrderState'),
    path('logout.html',views.logout,name='logout'),
    path('addProductToCart',views.addProductToCart,name='addProductToCart'),
    path('addOneProduct',views.addOneProduct,name='addOneProduct'),
    path('removeOneProduct',views.removeOneProduct,name='removeOneProduct'),
    path('interested',views.interested,name='interested'),
    path('contact_us',views.contact_us,name='contact_us'),
    path('delete_supp',views.delete_supp,name='delete_supp'),
    path('update_infos',views.update_infos,name='update_infos'),
    path('change_password',views.change_password,name='change_password'),
    path('update_discount',views.update_discount,name='update_discount'),
    path('create_supplier',views.create_supplier,name='create_supplier'),
    path('read_msg',views.read_msg,name='read_msg'),
    path('send_msg',views.send_msg,name='send_msg'),
    path('send_mail_to_client',views.send_mail_to_client,name='send_mail_to_client'),
    path('delete_msg',views.delete_msg,name='delete_msg'),
    path('add_new_product',views.add_new_product, name='add_new_product'),
    path('deleteProductFromCart',views.deleteProductFromCart,name='deleteProductFromCart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)