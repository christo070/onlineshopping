from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('sign-up/', views.signup, name='sigin-up'),
    path('login/', views.signin, name='login'),
    path('productdetail/', views.productdetail, name='productdetail'),


]
