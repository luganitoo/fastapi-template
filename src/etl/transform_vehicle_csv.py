import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

# Initialize the geolocator
geolocator = Nominatim(user_agent="vehicle_locator")

def get_address(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), language='en')
    
    if location:
        address_components = location.raw.get('address', {})
        state = address_components.get('state', '')
        city = address_components.get('city', '')
        street = address_components.get('road', '')
        print ('-------------------------------')
        print (address_components)
        print (state)
        print (city)
        print (street)
        print ('-------------------------------')
        return {
            'state': state,
            'city': city,
            'street': street
        }
    else:
        return None

def transform_data(raw_data):
    df = raw_data.copy()
    
    # Replace 'Null' with NaN for numeric columns
    numeric_columns = ['mileage', 'chargingpower', 'remainingelectricalrange', 'speed']
    df[numeric_columns] = df[numeric_columns].replace('Null', np.nan)

    # Convert to numeric types
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Delete rows with not enough information
    df = df.dropna(subset=['vin'])
    
    # Format DateTime
    df['datehour'] = df['datehour'].astype(str)
    date_format = '%d/%m/%Y %H:%M:%S'
    df['date_hour'] = pd.to_datetime(df['datehour'], errors='coerce', format=date_format)

    # Remove rows without a DateTime
    df = df.dropna(subset=['date_hour'])
    
    # Separete geolocation into 2 columns
    df[['latitude', 'longitude']] = df['geolocation'].str.split(',', expand=True).astype(float)
    
    # Add 'address' column with location information
    df['address'] = df.apply(lambda row: get_address(row['latitude'], row['longitude']), axis=1)

    # Interpolate missing data
    df['mileage'].fillna(df['mileage'].interpolate(), inplace=True)
    
    
    return df