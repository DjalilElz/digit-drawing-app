# Digit Drawing Data Collection App

A Django web application for collecting handwritten digit drawings, optimized for mobile devices.

## Features
- Interactive HTML5 canvas for drawing digits (0-9)
- Touch and mouse support
- Automatic data collection and storage
- Base64 image encoding
- PostgreSQL database support (Supabase)

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

## Database Structure

**DrawnDigit Model:**
- `digit_label`: Integer (0-9) - the digit that was drawn
- `image_data`: TextField - base64 encoded PNG image
- `created_at`: DateTime - timestamp of creation

## Exporting Data

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
