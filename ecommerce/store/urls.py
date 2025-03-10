from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/order/', views.place_order, name='place_order'),
    path("order-success/", views.order_success, name="order_success"),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
]
