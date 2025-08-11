from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import time
from .utils.debiaser import load_model, classify, debias

@api_view(["GET"])
def get_debiased_text(request):
    return JsonResponse({"debiased_text": "example"})

@api_view(["POST"])
def debias_text(request):
    text = request.data.get("text", "")
    try:
        load_model()
        text_classification = classify(text)
        debiased_text = debias(text, text_classification)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({
        "classification": text_classification,
        "debiased_text": debiased_text,
    })