from django.contrib import admin
from .models import Country, State, City, UserProfile

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_filter = ['country']
    search_fields = ['name', 'country__name']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'get_country']
    list_filter = ['state__country', 'state']
    search_fields = ['name', 'state__name', 'state__country__name']
    
    def get_country(self, obj):
        return obj.state.country.name
    get_country.short_description = 'Country'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profession', 'country', 'state', 'city', 'updated_at']
    list_filter = ['profession', 'country', 'state']
    search_fields = ['user__username', 'user__email', 'company_name']
    readonly_fields = ['created_at', 'updated_at']
