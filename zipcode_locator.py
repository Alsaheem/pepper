from opencage.geocoder import OpenCageGeocode

key = '0e8072ab89a445c09f4a1ae05b597ae4'

def get_zipcode_location(zipcode):
    geocoder = OpenCageGeocode(key)
    query=str(zipcode)
    results = geocoder.geocode(query)
    address = results[0]['formatted']
    latitude = results[0]['geometry']['lat']
    longitude = results[0]['geometry']['lng']
    return [address,longitude,latitude]
    
















# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="geoapiExercises")

# def get_zip_code_location(zipcode):
#     location = geolocator.geocode({"postalcode": zipcode})
#     if location is None:
#         print('location not available')
#         print('input another zipcode')
#         return None
#     else:
#         print(location.address)
#         print(location.longitude)
#         print(location.latitude)
#         return location.point
# print(get_zip_code_location(81929))