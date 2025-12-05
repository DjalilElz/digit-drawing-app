from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DrawnDigit
import json
import random

# Create your views here.

def index(request):
    # Generate a random digit for the user to draw
    random_digit = random.randint(0, 9)
    
    # Get count of saved drawings
    total_drawings = DrawnDigit.objects.count()
    
    context = {
        'digit_to_draw': random_digit,
        'total_drawings': total_drawings,
    }
    
    return render(request, 'home/index.html', context)

@csrf_exempt
def save_drawing(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            digit_label = data.get('digit')
            image_data = data.get('image')
            
            # Save to database
            drawn_digit = DrawnDigit.objects.create(
                digit_label=digit_label,
                image_data=image_data
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Drawing saved successfully!',
                'id': drawn_digit.id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

