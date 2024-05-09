"""
URL configuration for Agriculture_Website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    # ... your URL patterns here ...
    path ('cart/', views.CartPage ),
    path ('checkout/', views.CheckoutPage ),
    path ('addtocart/', views.add_to_cart ),
    path('cart/delete/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('create_order/', views.create_order, name='create_order'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('update_order_status/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),
]

