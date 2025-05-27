from django.core.management.base import BaseCommand
from profiles.models import Country, State, City

class Command(BaseCommand):
    help = 'Populate database with sample countries, states, and cities'

    def handle(self, *args, **options):
        # Clear existing data
        City.objects.all().delete()
        State.objects.all().delete()
        Country.objects.all().delete()

        # Create countries
        countries_data = [
            {'name': 'United States', 'code': 'US'},
            {'name': 'Canada', 'code': 'CA'},
            {'name': 'United Kingdom', 'code': 'GB'},
            {'name': 'India', 'code': 'IN'},
            {'name': 'Australia', 'code': 'AU'},
            {'name': 'Germany', 'code': 'DE'},
            {'name': 'France', 'code': 'FR'},
            {'name': 'Japan', 'code': 'JP'},
            {'name': 'Brazil', 'code': 'BR'},
            {'name': 'Mexico', 'code': 'MX'},
        ]

        countries = {}
        for country_data in countries_data:
            country = Country.objects.create(**country_data)
            countries[country.code] = country
            self.stdout.write(f'Created country: {country.name}')

        # Create states/provinces
        states_data = {
            'US': [
                'California', 'New York', 'Texas', 'Florida', 'Illinois',
                'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan'
            ],
            'CA': [
                'Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba',
                'Saskatchewan', 'Nova Scotia', 'New Brunswick', 'Newfoundland and Labrador', 'Prince Edward Island'
            ],
            'GB': [
                'England', 'Scotland', 'Wales', 'Northern Ireland'
            ],
            'IN': [
                'Maharashtra', 'Tamil Nadu', 'Karnataka', 'Gujarat', 'Rajasthan',
                'West Bengal', 'Madhya Pradesh', 'Uttar Pradesh', 'Delhi', 'Punjab'
            ],
            'AU': [
                'New South Wales', 'Victoria', 'Queensland', 'Western Australia',
                'South Australia', 'Tasmania', 'Australian Capital Territory', 'Northern Territory'
            ],
            'DE': [
                'Bavaria', 'North Rhine-Westphalia', 'Baden-Württemberg', 'Lower Saxony',
                'Hesse', 'Saxony', 'Rhineland-Palatinate', 'Schleswig-Holstein'
            ],
            'FR': [
                'Île-de-France', 'Auvergne-Rhône-Alpes', 'Hauts-de-France', 'Nouvelle-Aquitaine',
                'Occitanie', 'Grand Est', 'Provence-Alpes-Côte d\'Azur', 'Pays de la Loire'
            ],
            'JP': [
                'Tokyo', 'Osaka', 'Kanagawa', 'Aichi', 'Saitama',
                'Chiba', 'Hyogo', 'Hokkaido', 'Fukuoka', 'Kyoto'
            ],
            'BR': [
                'São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Bahia', 'Paraná',
                'Rio Grande do Sul', 'Pernambuco', 'Ceará', 'Pará', 'Santa Catarina'
            ],
            'MX': [
                'Mexico City', 'Jalisco', 'Nuevo León', 'Puebla', 'Guanajuato',
                'Chihuahua', 'Baja California', 'Veracruz', 'Michoacán', 'Oaxaca'
            ]
        }

        states = {}
        for country_code, state_names in states_data.items():
            country = countries[country_code]
            for state_name in state_names:
                state = State.objects.create(name=state_name, country=country)
                states[f'{country_code}_{state_name}'] = state
                self.stdout.write(f'Created state: {state_name} in {country.name}')

        # Create cities
        cities_data = {
            'US_California': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'San Jose'],
            'US_New York': ['New York City', 'Buffalo', 'Rochester', 'Syracuse', 'Albany'],
            'US_Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'],
            'CA_Ontario': ['Toronto', 'Ottawa', 'Hamilton', 'London', 'Windsor'],
            'CA_Quebec': ['Montreal', 'Quebec City', 'Laval', 'Gatineau', 'Longueuil'],
            'GB_England': ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Leeds'],
            'IN_Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad'],
            'IN_Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool'],
            'IN_Arunachal Pradesh': ['Itanagar', 'Tawang', 'Ziro', 'Pasighat', 'Bomdila'],
            'IN_Assam': ['Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat', 'Nagaon'],
            'IN_Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Purnia'],
            'IN_Delhi': ['New Delhi', 'Old Delhi', 'Dwarka', 'Rohini', 'Saket'],
            'IN_Chhattisgarh': ['Raipur', 'Bhilai', 'Bilaspur', 'Korba', 'Durg'],
            'IN_Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem'],
            'AU_New South Wales': ['Sydney', 'Newcastle', 'Wollongong', 'Albury', 'Tamworth'],
            'DE_Bavaria': ['Munich', 'Nuremberg', 'Augsburg', 'Würzburg', 'Regensburg'],
        }

        for state_key, city_names in cities_data.items():
            if state_key in states:
                state = states[state_key]
                for city_name in city_names:
                    city = City.objects.create(name=city_name, state=state)
                    self.stdout.write(f'Created city: {city_name} in {state.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with '
                f'{Country.objects.count()} countries, '
                f'{State.objects.count()} states, and '
                f'{City.objects.count()} cities'
            )
        )
