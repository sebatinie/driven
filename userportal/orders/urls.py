from django.urls import path
from .views import get_order

urlpatterns = [
    path('orders/<str:order_id>/', get_order),
]

