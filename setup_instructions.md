# Multi-Step User Profile Update Form - Setup Instructions

## Prerequisites
- Python 3.8+
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)

## Setup Steps

### 1. Create Django Project
\`\`\`bash
django-admin startproject profile_project
cd profile_project
\`\`\`

### 2. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure MongoDB
- Update `DATABASES` configuration in `settings.py` with your MongoDB connection string
- For MongoDB Atlas, replace the connection string with your cluster URL

### 4. Create Database Tables
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

### 5. Populate Sample Data
\`\`\`bash
python manage.py populate_locations
\`\`\`

### 6. Create Superuser (Optional)
\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 7. Create Media Directory
\`\`\`bash
mkdir media
mkdir media/profile_images
\`\`\`

### 8. Run Development Server
\`\`\`bash
python manage.py runserver
\`\`\`

### 9. Access the Application
- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Register: http://127.0.0.1:8000/register/
- Login: http://127.0.0.1:8000/login/

## Features Implemented

✅ Multi-step form with progress indicator
✅ Real-time username availability check
✅ Password strength meter with validation
✅ Image upload with live preview and validation
✅ Conditional form fields (company details for entrepreneurs)
✅ Cascading dropdowns (Country → State → City)
✅ Client and server-side validation
✅ Session-based form data persistence
✅ MongoDB integration using djongo
✅ Bootstrap responsive design
✅ AJAX-powered dynamic fields

## API Endpoints

- `/api/check-username/?username=<username>` - Check username availability
- `/api/states/?country=<country_id>` - Get states for a country
- `/api/cities/?state=<state_id>` - Get cities for a state

## File Structure

\`\`\`
profile_project/
├── manage.py
├── requirements.txt
├── profile_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── profiles/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── management/
│       └── commands/
│           └── populate_locations.py
├── templates/
│   ├── base.html
│   └── profiles/
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── profile_update.html
│       └── profile_view.html
└── media/
    └── profile_images/
\`\`\`

## Deployment Notes

### For Render/Heroku:
1. Add `gunicorn` to requirements.txt
2. Create `Procfile`: `web: gunicorn profile_project.wsgi`
3. Set environment variables for MongoDB connection
4. Configure static files collection
5. Update `ALLOWED_HOSTS` in settings.py

### Environment Variables:
- `DJANGO_SECRET_KEY`: Your Django secret key
- `MONGODB_URI`: Your MongoDB connection string
- `DEBUG`: Set to False for production
