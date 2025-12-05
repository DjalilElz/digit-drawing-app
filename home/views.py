from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import DrawnDigit
import json
import random

# Create your views here.

def index(request):
    # Generate a random digit for the user to draw
    random_digit = random.randint(0, 9)
    
    # Get count of saved drawings
    total_drawings = DrawnDigit.objects.count()
    
    # Get top 10 leaderboard
    leaderboard = DrawnDigit.objects.values('username').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'digit_to_draw': random_digit,
        'total_drawings': total_drawings,
        'leaderboard': leaderboard,
    }
    
    return render(request, 'home/index.html', context)

@csrf_exempt
def save_drawing(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            digit_label = data.get('digit')
            image_data = data.get('image')
            username = data.get('username', 'Anonymous').strip() or 'Anonymous'
            
            # Save to database
            drawn_digit = DrawnDigit.objects.create(
                username=username,
                digit_label=digit_label,
                image_data=image_data
            )
            
            # Get updated user stats
            user_count = DrawnDigit.objects.filter(username=username).count()
            total_count = DrawnDigit.objects.count()
            
            # Generate new digit
            new_digit = random.randint(0, 9)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Drawing saved successfully!',
                'id': drawn_digit.id,
                'user_count': user_count,
                'total_count': total_count,
                'new_digit': new_digit
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def get_leaderboard(request):
    leaderboard = DrawnDigit.objects.values('username').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    return JsonResponse({
        'leaderboard': list(leaderboard)
    })

