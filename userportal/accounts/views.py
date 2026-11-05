from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .services import fetch_user_data


def user_detail(request, user_id):

    result = fetch_user_data(user_id)

    return JsonResponse(result)