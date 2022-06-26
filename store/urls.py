from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_item/',views.processItem,name="process_item"),
    path('login/',views.login,name="login"),
    path('createUser/',views.createUser,name="createUser"),
    path('logout/',views.logout,name="logout"),
]
