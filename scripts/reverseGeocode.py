# import necessary modules
import pandas as pd
import json, requests

# load the gps coordinate data
df = pd.read_csv('openpaths_cortylal.csv')

# create new columns
df['geocode_data'] = ''
df['city'] = ''
df['country'] = ''

df.head()

# function that handles the geocoding requests
def reverseGeocode(latlng):
    
    result = {}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}'
    apikey = 'AIzaSyDcKzu3KZBJxQ-1chbvrIlW7cKchhOJ_uw'
    
    request = url.format(latlng, apikey)
    data = json.loads(requests.get(request).text)
    if len(data['results']) > 0:
        result = data['results'][0]

    return result


for i, row in df.iterrows():
    # for each row in the dataframe, geocode the lat-long data
    df['geocode_data'][i] = reverseGeocode(df['lat'][i].astype(str) + ',' + df['lon'][i].astype(str))

# identify municipality and country data in the blob that google sent back
for i, row in df.iterrows():
    if 'address_components' in row['geocode_data']:
        
        # first try to identify the country
        for component in row['geocode_data']['address_components']:
            if 'country' in component['types']:
                df['country'][i] = component['long_name']
        
        # now try to identify the municipality
        for component in row['geocode_data']['address_components']:
            if 'locality' in component['types']:
                df['city'][i] = component['long_name']
                break
            elif 'postal_town' in component['types']:
                df['city'][i] = component['long_name']
                break
            elif 'administrative_area_level_2' in component['types']:
                df['city'][i] = component['long_name']
                break
            elif 'administrative_area_level_1' in component['types']:
                df['city'][i] = component['long_name']
                break

df1 = df[['lat','lon','alt','date','city','country']]
df1.to_csv('geocoded_openpaths_data.csv', encoding='utf-8', index=False)