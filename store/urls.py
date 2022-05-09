from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('sign-up/', views.signup, name='sign-up'),
    path('signout/', views.signout, name='signout'),
    path('login/', views.signin, name='login'),
    path('productdetail/<int:id>', views.productdetail, name='productdetail'),
    path('update_item/', views.updateItem, name='update_item'),
    path('checksignedin/', views.checksignedin, name='checksignedin'),
]
