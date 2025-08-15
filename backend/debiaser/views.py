from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import time
from .utils.debiaser import load_model, classify, debias
from django.core.cache import cache
import os
from dotenv import load_dotenv
load_dotenv()

cooldown_key = "debias_text_last_call"
previous_calls_key = "debias_text_num_previous_calls"
calls_per_hour_limit = int(os.getenv("DEBIAS_RATE_LIMIT_PER_HOUR", 20))
cooldown_seconds = int(os.getenv("DEBIAS_COOLDOWN_SECONDS", 10))

@api_view(["POST"])
def debias_text(request):
    cooldown_check = check_cooldown()
    if cooldown_check:
        return cooldown_check

    text = request.data.get("text", "")
    try:
        load_model()
        text_classification = classify(text)
        debiased_text = debias(text, text_classification)
    except Exception as e:
        print("###########ERROR###########")
        print(e)
        return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({
        "classification": text_classification,
        "debiased_text": debiased_text,
    })

def check_cooldown():
    global previous_calls_key, cooldown_seconds, calls_per_hour_limit, cooldown_key
    previous_calls = cache.get(previous_calls_key)
    if previous_calls is None:
        cache.set(previous_calls_key, 1, 3600)  # Reset count every hour
    elif previous_calls >= calls_per_hour_limit:
        print("###########RATE_LIMITED###########")
        return JsonResponse({"error": f"Rate limit exceeded (more than {calls_per_hour_limit} calls per hour made)"}, status=429)
    else:
        cache.incr(previous_calls_key, 1)
    
    last_call = cache.get(cooldown_key)
    now = time.time()

    if last_call is None:
        cache.set(cooldown_key, now)
        return
    if now - last_call < cooldown_seconds:
        wait_time = cooldown_seconds - (now - last_call)
        print("###########COOLDOWN###########")
        return JsonResponse({"error": f"Please wait {wait_time:.1f} seconds before retrying"}, status=429)
    cache.set(cooldown_key, now)
