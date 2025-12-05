from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import DrawnDigit
import json
import random
import base64
from io import BytesIO
from PIL import Image

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
            
            # Convert base64 to PIL Image
            image_data_base64 = image_data.split(',')[1]  # Remove data:image/png;base64, prefix
            image_bytes = base64.b64decode(image_data_base64)
            img = Image.open(BytesIO(image_bytes))
            
            # Convert to grayscale and resize to 28x28
            img = img.convert('L')  # Convert to grayscale
            img_resized = img.resize((28, 28), Image.Resampling.LANCZOS)
            
            # Convert back to base64
            buffered = BytesIO()
            img_resized.save(buffered, format="PNG")
            img_28x28_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            img_28x28_data = f"data:image/png;base64,{img_28x28_base64}"
            
            # Save to database with 28x28 image
            drawn_digit = DrawnDigit.objects.create(
                username=username,
                digit_label=digit_label,
                image_data=img_28x28_data
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

