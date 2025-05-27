from django.db import models
from django.contrib.auth.models import User
from countries.models import Country, State, City

def user_profile_image_path(instance, filename):
    return f'profile_pictures/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    PROFESSION_CHOICES = [
        ('student', 'Student'),
        ('developer', 'Developer'),
        ('entrepreneur', 'Entrepreneur'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    SUBSCRIPTION_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_profile_image_path, blank=False, null=False)
    
    # Personal Details
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    custom_gender = models.CharField(max_length=50, blank=True, help_text="Specify if gender is 'Other'")
    date_of_birth = models.DateField(null=True, blank=True)  # Keep this field
    
    # Professional Details
    profession = models.CharField(max_length=20, choices=PROFESSION_CHOICES, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    
    # Address
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)  # Keep this field
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Preferences
    subscription_plan = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='basic')
    newsletter = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
