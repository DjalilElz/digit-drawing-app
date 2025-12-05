# Handwritten Digit Collection Challenge 🎯

A Django web application designed to collect handwritten digit samples for Machine Learning research and Deep Learning projects. This gamified data collection platform allows users to compete while contributing valuable training data for handwriting recognition models.

## 🎓 Project Purpose

This application is part of an Artificial Intelligence research project for Deep Learning studies. The goal is to collect diverse handwriting samples from different users to:

- Train and improve digit recognition models
- Study handwriting pattern variations across users
- Build datasets for machine learning projects
- Research human handwriting behavior

Each contribution helps advance AI research and education. Thank you for participating! 🙏

## ✨ Features

- **🎨 Interactive Drawing Canvas**: HTML5 canvas (280×280) with touch and mouse support
- **🏆 Competition Mode**: Users compete on a leaderboard by contributing more samples
- **👤 User Tracking**: Personal counters and username persistence
- **📊 Real-time Leaderboard**: Top 10 contributors with live updates
- **🖼️ Smart Image Processing**: Automatic resize to 28×28 grayscale (MNIST-compatible)
- **💾 Dual Format Storage**: Keeps original 280×280 submissions + generates 28×28 for ML
- **⚡ Instant Feedback**: No page reloads, immediate response after submission
- **🎲 Random Digit Assignment**: Ensures balanced dataset collection
- **📱 Mobile Optimized**: Responsive design for all devices
- **☁️ Cloud Database**: PostgreSQL via Supabase for scalable storage

## 🔧 Technical Stack

- **Backend**: Django 6.0
- **Database**: PostgreSQL (Supabase)
- **Image Processing**: Pillow (PIL)
- **Deployment**: Render.com
- **Static Files**: WhiteNoise
- **Server**: Gunicorn

## Local Development

1. Create virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to use the app.

## Deployment to Render with Supabase

### Step 1: Set up Supabase Database

1. Go to [Supabase](https://supabase.com) and create an account
2. Create a new project
3. Go to Project Settings > Database
4. Copy the Connection String (URI format)
   - It looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

### Step 2: Deploy to Render

1. Push your code to GitHub
2. Go to [Render](https://render.com) and sign up
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: digit-drawing-app (or your choice)
   - **Runtime**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn mysite.wsgi:application`

### Step 3: Set Environment Variables in Render

In Render dashboard, add these environment variables:

- `DATABASE_URL` = Your Supabase connection string
- `SECRET_KEY` = Generate a new secret key (use Django's `get_random_secret_key()`)
- `DEBUG` = `False`
- `ALLOWED_HOSTS` = Your Render app URL (e.g., `your-app-name.onrender.com`)
- `PYTHON_VERSION` = `3.14.0`

### Step 4: Deploy

Click "Create Web Service" and wait for deployment to complete.

## Environment Variables

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Django secret key for security
- `DATABASE_URL`: PostgreSQL connection string from Supabase
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## 📊 Database Structure

**DrawnDigit Model:**
- `id`: Primary key
- `username`: CharField - contributor's name (default: 'Anonymous')
- `digit_label`: Integer (0-9) - the digit that was drawn
- `image_data`: TextField - base64 encoded PNG image (28×28 grayscale for new submissions)
- `created_at`: DateTime - timestamp of creation

**Note**: Old submissions (280×280) remain unchanged. New submissions are automatically resized to 28×28 grayscale for ML compatibility.

## 📦 Exporting Data for Machine Learning

Use the built-in management command to export collected data:

### Export as JSON (includes all metadata)
```bash
python manage.py export_digits --output my_dataset.json --format json --resize 28
```

### Export as NumPy arrays (requires numpy)
```bash
pip install numpy
python manage.py export_digits --output my_dataset.npz --format numpy --resize 28
```

### Options:
- `--output`: Output file path (default: `digits_export.json`)
- `--format`: `json` or `numpy` (default: `json`)
- `--resize`: Resize all images to `28` or `280` (default: `28`)

### Using the exported data:

**JSON format:**
```python
import json

with open('my_dataset.json', 'r') as f:
    data = json.load(f)

for sample in data:
    print(f"User: {sample['username']}, Label: {sample['label']}")
```

**NumPy format:**
```python
import numpy as np

data = np.load('my_dataset.npz')
images = data['images']  # Shape: (N, 28, 28)
labels = data['labels']   # Shape: (N,)
usernames = data['usernames']  # Shape: (N,)

print(f"Dataset size: {len(images)} samples")
print(f"Image shape: {images[0].shape}")
```

## 🎮 How It Works

1. **User enters name** → Stored in localStorage for persistence
2. **Random digit displayed** → Ensures balanced data collection
3. **User draws on canvas** → 280×280 touch/mouse enabled
4. **Submit drawing** → Converts to 28×28 grayscale + saves both formats
5. **Instant feedback** → New digit + updated stats without page reload
6. **Leaderboard updates** → Top 10 refreshes every 10 seconds

## 🚀 Deployment Notes

To export collected drawings for machine learning:

```python
python manage.py shell
from home.models import DrawnDigit
import base64
from PIL import Image
from io import BytesIO

# Export all drawings
for digit in DrawnDigit.objects.all():
    image_data = digit.image_data.split(',')[1]
    img = Image.open(BytesIO(base64.b64decode(image_data)))
    img.save(f'digit_{digit.digit_label}_{digit.id}.png')
```

## Tech Stack

- Django 6.0
- PostgreSQL (Supabase)
- Gunicorn
- WhiteNoise
- HTML5 Canvas
- Vanilla JavaScript
