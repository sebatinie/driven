from django.urls import path
from .views import user_detail

urlpatterns = [
    path('user/<int:user_id>/', user_detail),
]

