from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import UserProfile, Country, State, City
from .forms import Step1PersonalForm, Step2ProfessionalForm, Step3PreferencesForm
import json

def home(request):
    return render(request, 'profiles/home.html')

@login_required
def profile_update(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get current step from session or default to 1
    current_step = request.session.get('profile_update_step', 1)
    
    if request.method == 'POST':
        if current_step == 1:
            form = Step1PersonalForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                request.session['step1_data'] = {
                    'username': form.cleaned_data['username'],
                    'new_password': form.cleaned_data.get('new_password', ''),
                }

                # Update User object
                user = request.user
                if user.username != form.cleaned_data['username']:
                    user.username = form.cleaned_data['username']
                    user.save()

                # Get or create profile
                profile, _ = UserProfile.objects.get_or_create(user=user)

                # Save gender and custom_gender
                profile.gender = form.cleaned_data['gender']
                profile.custom_gender = form.cleaned_data['custom_gender']

                # Save profile picture
                if form.cleaned_data.get('profile_picture'):
                    if profile.profile_picture:
                        profile.delete_old_profile_picture()
                    profile.profile_picture = form.cleaned_data['profile_picture']

                profile.save()

                request.session['profile_update_step'] = 2
                messages.success(request, 'Personal information saved! Continue to professional details.')
                return redirect('profile_update')

        
        elif current_step == 2:
            form = Step2ProfessionalForm(request.POST)
            if form.is_valid():
                # Save step 2 data to session
                request.session['step2_data'] = {
                    'profession': form.cleaned_data['profession'],
                    'company_name': form.cleaned_data.get('company_name', ''),
                    'company_address': form.cleaned_data.get('company_address', ''),
                    'address_line1': form.cleaned_data['address_line1'],
                    'address_line2': form.cleaned_data.get('address_line2', ''),
                }
                request.session['profile_update_step'] = 3
                messages.success(request, 'Professional details saved! Complete your preferences.')
                return redirect('profile_update')
        
        elif current_step == 3:
            form = Step3PreferencesForm(request.POST)
            if form.is_valid():
                # Save all data to database
                try:
                    # Update user data from step 1
                    step1_data = request.session.get('step1_data', {})
                    if step1_data.get('username') and step1_data['username'] != request.user.username:
                        request.user.username = step1_data['username']
                    if step1_data.get('new_password'):
                        request.user.set_password(step1_data['new_password'])
                        # Re-authenticate user after password change
                        user = authenticate(username=request.user.username, password=step1_data['new_password'])
                        if user:
                            login(request, user)
                    request.user.save()
                    
                    # Update profile data from step 2
                    step2_data = request.session.get('step2_data', {})
                    profile.profession = step2_data.get('profession', '')
                    profile.company_name = step2_data.get('company_name', '')
                    profile.company_address = step2_data.get('company_address', '')
                    profile.address_line1 = step2_data.get('address_line1', '')
                    profile.address_line2 = step2_data.get('address_line2', '')
                    
                    # Update profile data from step 3
                    profile.country = form.cleaned_data.get('country')
                    profile.state = form.cleaned_data.get('state')
                    profile.city = form.cleaned_data.get('city')
                    profile.date_of_birth = form.cleaned_data.get('date_of_birth')
                    
                    profile.save()
                    
                    # Clear session data
                    for key in ['step1_data', 'step2_data', 'profile_update_step']:
                        request.session.pop(key, None)
                    
                    messages.success(request, 'Profile updated successfully!')
                    return redirect('profile_view')
                
                except Exception as e:
                    messages.error(request, f'Error updating profile: {str(e)}')
    
    else:
        initial_data = {}  # <-- Ensure it's always defined

    # Initialize forms with existing data
    if current_step == 1:
        initial_data = {
            'username': request.user.username,
        }
        form = Step1PersonalForm(initial=initial_data, user=request.user)

    elif current_step == 2:
        initial_data = {
            'profession': profile.profession,
            'company_name': profile.company_name,
            'company_address': profile.company_address,
            'address_line1': profile.address_line1,
            'address_line2': profile.address_line2,
        }
        form = Step2ProfessionalForm(initial=initial_data)

    elif current_step == 3:
        initial_data = {
            'country': profile.country,
            'state': profile.state,
            'city': profile.city,
            'date_of_birth': profile.date_of_birth,
        }
        form = Step3PreferencesForm(initial=initial_data)

    context = {
    'form': form,
    'current_step': current_step,
    'profile': profile,
    }

    return render(request, 'profiles/profile_update.html', context)


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profiles/profile_view.html', {'profile': profile})

# API Views
def check_username(request):
    username = request.GET.get('username', '')
    current_user = request.user if request.user.is_authenticated else None
    
    if current_user and username == current_user.username:
        return JsonResponse({'available': True})
    
    if len(username) < 3:
        return JsonResponse({'available': False, 'message': 'Username must be at least 3 characters'})
    
    available = not User.objects.filter(username=username).exists()
    return JsonResponse({'available': available})

def get_states(request):
    country_id = request.GET.get('country')
    if not country_id or not country_id.isdigit():
        return JsonResponse({'states': []})
    states = State.objects.filter(country_id=country_id).values('id', 'name').order_by('name')
    return JsonResponse({'states': list(states)})

def get_cities(request):
    state_id = request.GET.get('state')
    if not state_id or not state_id.isdigit():
        return JsonResponse({'cities': []})
    cities = City.objects.filter(state_id=state_id).values('id', 'name').order_by('name')
    return JsonResponse({'cities': list(cities)})

# Simple auth views for testing
def simple_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profile_update')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'profiles/login.html')

def simple_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if not username or not password:
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            try:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                messages.success(request, f'Welcome {user.username}! Please complete your profile.')
                return redirect('profile_update')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'profiles/register.html')





def profile_summary(request):
    return render(request, 'profiles/profile_summary.html')  # make sure this template exists


