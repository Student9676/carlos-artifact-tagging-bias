from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def debias_text(request):
    text = request.data.get('text', '')
    debiased_text = "debiased text: " + text # placeholder
    return Response({'debiased_text': debiased_text})