from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import UserProfile, Country, State, City
import re
from PIL import Image

class Step1PersonalForm(forms.Form):
    profile_picture = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png',
            'id': 'profile-picture-input'
        }),
        help_text='Required: JPG/PNG format only'
    )
    username = forms.CharField(
        min_length=4,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username-input',
            'placeholder': 'Enter username (4-20 characters, no spaces)'
        })
    )
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'gender-select'
        })
    )
    custom_gender = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'custom-gender-input',
            'placeholder': 'Please specify your gender',
            'style': 'display: none;'
        })
    )
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter current password (required for password change)'
        })
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'new-password-input',
            'placeholder': 'Enter new password (8+ chars, 1 special char, 1 number)'
        })
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            # Make profile picture not required if user already has one
            try:
                profile = UserProfile.objects.get(user=self.user)
                if profile.profile_picture:
                    self.fields['profile_picture'].required = False
                    self.fields['profile_picture'].help_text = 'Upload new image to replace current one'
            except UserProfile.DoesNotExist:
                pass
    
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Check file size (2MB limit)
            if picture.size > 2 * 1024 * 1024:
                raise ValidationError("Image file too large ( > 2MB )")
            
            # Check file type
            if not picture.content_type in ['image/jpeg', 'image/png']:
                raise ValidationError("Only JPEG and PNG images are allowed.")
            
            # Validate image using PIL
            try:
                img = Image.open(picture)
                img.verify()
            except Exception:
                raise ValidationError("Invalid image file.")
        
        return picture
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Check for spaces
        if ' ' in username:
            raise ValidationError("Username cannot contain spaces.")
        
        # Check if username is taken by another user
        if self.user and username != self.user.username:
            if User.objects.filter(username=username).exists():
                raise ValidationError("This username is already taken.")
        elif not self.user:
            if User.objects.filter(username=username).exists():
                raise ValidationError("This username is already taken.")
        
        return username
    
    def clean_custom_gender(self):
        gender = self.cleaned_data.get('gender')
        custom_gender = self.cleaned_data.get('custom_gender')
        
        if gender == 'other' and not custom_gender:
            raise ValidationError("Please specify your gender when selecting 'Other'.")
        
        return custom_gender
    
    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        if password:
            # Password strength validation
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise ValidationError("Password must contain at least one special character.")
            if not re.search(r'\d', password):
                raise ValidationError("Password must contain at least one number.")
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # If new password is provided, current password is required
        if new_password and not current_password:
            raise ValidationError("Current password is required to set a new password.")
        
        # Verify current password
        if current_password and self.user:
            if not authenticate(username=self.user.username, password=current_password):
                raise ValidationError("Current password is incorrect.")
        
        # Check password confirmation
        if new_password and new_password != confirm_password:
            raise ValidationError("New passwords do not match.")
        
        return cleaned_data

class Step2ProfessionalForm(forms.Form):
    profession = forms.ChoiceField(
        choices=UserProfile.PROFESSION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'profession-select'
        })
    )
    company_name = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'company-name-input',
            'placeholder': 'Enter company name'
        })
    )
    address_line1 = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your address'
        })
    )
    address_line2 = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter address line 2 (optional)'
        })
    )
    
    def clean_company_name(self):
        profession = self.cleaned_data.get('profession')
        company_name = self.cleaned_data.get('company_name')
        
        if profession == 'entrepreneur' and not company_name:
            raise ValidationError("Company name is required for entrepreneurs.")
        
        return company_name

class Step3PreferencesForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label="Select Country",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'country-select'
        })
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.none(),
        empty_label="Select State",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'state-select'
        })
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        empty_label="Select City",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'city-select'
        })
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date-of-birth'
        })
    )
    subscription_plan = forms.ChoiceField(
    choices=UserProfile.SUBSCRIPTION_CHOICES,
    widget=forms.RadioSelect(attrs={
        'class': 'form-check-input'
    })
    )

    newsletter = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'newsletter-checkbox'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.initial.get('country'):
            self.fields['state'].queryset = State.objects.filter(country=self.initial['country']).order_by('name')
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.initial.get('state'):
            self.fields['city'].queryset = City.objects.filter(state=self.initial['state']).order_by('name')

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            from datetime import date
            if dob > date.today():
                raise ValidationError("Date of birth cannot be in the future.")
        return dob
