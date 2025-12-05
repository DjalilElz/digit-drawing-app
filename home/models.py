from django.db import models

# Create your models here.

class DrawnDigit(models.Model):
    username = models.CharField(max_length=100, default='Anonymous')
    digit_label = models.IntegerField(help_text="The digit number (0-9)")
    image_data = models.TextField(help_text="Base64 encoded image data")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - Digit {self.digit_label} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
