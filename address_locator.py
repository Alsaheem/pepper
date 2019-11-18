from opencage.geocoder import OpenCageGeocode

key = '0e8072ab89a445c09f4a1ae05b597ae4'

def get_address_location(city):
    geocoder = OpenCageGeocode(key)
    query=str(city)
    results = geocoder.geocode(query)
    address = results[0]['formatted']
    latitude = results[0]['geometry']['lat']
    longitude = results[0]['geometry']['lng']
    return [address,longitude,latitude]