from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import time

@api_view(['GET'])
def get_debiased_text(request):
    return JsonResponse({'debiased_text': "example"})

@api_view(['POST'])
def debias_text(request):
    text = request.data.get('text', '')
    time.sleep(10)
    debiased_text = "DEBIASED->" + text # placeholder
    return JsonResponse({'debiased_text': debiased_text})

