from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Search
from .forms import SearchForm
import folium
import geocoder



# Create your views here.

def indexFun(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        
        if form.is_valid():
            form.save()
        return redirect(indexFun)
    else:
        form = SearchForm()

    # Attempt to get the last address from the database
    address = Search.objects.all().last()
    print(address, "llllllll")
    
    # Attempt to geocode the address
    location = geocoder.osm(address)
    lat = location.lat
    lng = location.lng
    country = location.country
    
    if lat is None or lng is None:
        # If geocoding fails, find the last valid address with valid lat and lng
        valid_location = None
        for addr in Search.objects.all().reverse():
            location = geocoder.osm(addr)
            if location.lat is not None and location.lng is not None:
                valid_location = location
                break
        
        if valid_location is None:
            return HttpResponse('Your Address Input Is Invalid')
        else:
            lat = valid_location.lat
            lng = valid_location.lng
            country = valid_location.country

    # Create Map Object
    m = folium.Map(location=[lat, lng], zoom_start=1)
    
    # Add marker to the map
    folium.Marker([lat, lng], tooltip='Click for more', popup=country).add_to(m)
    
    # Get HTML representation of the map object
    m = m._repr_html_()
    
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)


from geopy.geocoders import Nominatim

def index(request):
    return render(request, 'map.html')

def get_location(request):
    coordinates = None
    address = None
    if request.method == 'POST':
        address = request.POST.get('address')
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(address)
        if location:
            coordinates = (location.latitude, location.longitude)
    return render(request, 'map.html', {'coordinates': coordinates, 'address': address})
