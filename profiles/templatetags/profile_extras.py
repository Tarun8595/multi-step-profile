from django import template

register = template.Library()

@register.filter
def profile_completion(profile):
    """Calculate profile completion percentage"""
    total_fields = 8
    completed_fields = 0
    
    # Check each field
    if profile.profile_picture:
        completed_fields += 1
    if profile.profession:
        completed_fields += 1
    if profile.address_line1:
        completed_fields += 1
    if profile.country:
        completed_fields += 1
    if profile.state:
        completed_fields += 1
    if profile.city:
        completed_fields += 1
    if profile.date_of_birth:
        completed_fields += 1
    if profile.company_name and profile.profession == 'entrepreneur':
        completed_fields += 1
    
    return int((completed_fields / total_fields) * 100)
