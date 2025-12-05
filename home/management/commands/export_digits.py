"""
Management command to export digit drawings for machine learning.

Usage:
    python manage.py export_digits --output digits_export.json
    python manage.py export_digits --output digits.npz --format numpy
"""

from django.core.management.base import BaseCommand
from home.models import DrawnDigit
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np


class Command(BaseCommand):
    help = 'Export digit drawings for machine learning projects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='digits_export.json',
            help='Output file path'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'numpy'],
            default='json',
            help='Export format: json or numpy'
        )
        parser.add_argument(
            '--resize',
            type=int,
            choices=[28, 280],
            default=28,
            help='Resize all images to this size (28 or 280)'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        export_format = options['format']
        target_size = options['resize']

        self.stdout.write(f'Exporting digits to {output_file}...')
        
        digits = DrawnDigit.objects.all().order_by('created_at')
        total = digits.count()
        
        if total == 0:
            self.stdout.write(self.style.WARNING('No digits found in database.'))
            return

        if export_format == 'json':
            self._export_json(digits, output_file, target_size, total)
        else:
            self._export_numpy(digits, output_file, target_size, total)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported {total} digits!'))

    def _export_json(self, digits, output_file, target_size, total):
        """Export as JSON file"""
        data = []
        
        for i, digit in enumerate(digits, 1):
            if i % 100 == 0:
                self.stdout.write(f'Processing {i}/{total}...')
            
            # Get image data
            img_data = self._process_image(digit.image_data, target_size)
            
            data.append({
                'id': digit.id,
                'username': digit.username,
                'label': digit.digit_label,
                'image': img_data,
                'created_at': digit.created_at.isoformat(),
            })
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _export_numpy(self, digits, output_file, target_size, total):
        """Export as NumPy .npz file (requires numpy)"""
        try:
            images = []
            labels = []
            usernames = []
            
            for i, digit in enumerate(digits, 1):
                if i % 100 == 0:
                    self.stdout.write(f'Processing {i}/{total}...')
                
                # Convert base64 to numpy array
                img_array = self._image_to_array(digit.image_data, target_size)
                
                images.append(img_array)
                labels.append(digit.digit_label)
                usernames.append(digit.username)
            
            # Save as compressed numpy file
            np.savez_compressed(
                output_file,
                images=np.array(images),
                labels=np.array(labels),
                usernames=np.array(usernames)
            )
            
            self.stdout.write(f'Saved {len(images)} images with shape {images[0].shape}')
            
        except ImportError:
            self.stdout.write(self.style.ERROR('NumPy is required for numpy format. Install it with: pip install numpy'))

    def _process_image(self, image_data, target_size):
        """Process image and return base64 string at target size"""
        # Decode base64
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        img = Image.open(BytesIO(image_bytes))
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Resize if needed
        if img.size != (target_size, target_size):
            img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
        
        # Convert back to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return f"data:image/png;base64,{img_base64}"

    def _image_to_array(self, image_data, target_size):
        """Convert base64 image to numpy array"""
        # Decode base64
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        img = Image.open(BytesIO(image_bytes))
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Resize if needed
        if img.size != (target_size, target_size):
            img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        return np.array(img)
