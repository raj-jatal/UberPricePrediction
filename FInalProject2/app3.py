import pickle
import streamlit as st
import pandas as pd
from geopy import distance


# Load the pickled model
model_file = open('regressor', 'rb')
model = pickle.load(model_file)

# Set page title and favicon
st.set_page_config(page_title='Cab Price Prediction App', page_icon=':car:')

# Add heading with background color and heading color
st.markdown("<h1 style='text-align: center; color: white;'>&#x1F697; Cab Price Prediction App</h1>", unsafe_allow_html=True)

# Add gap
st.empty()


# Define the input fields
st.sidebar.header('Enter the following values:')
# distance = st.sidebar.number_input('Distance')
source = st.sidebar.selectbox('Source', ['Back Bay', 'Beacon Hill', 'Boston University', 'Fenway', 'Financial District', 'Haymarket Square', 'North End', 'North Station', 'Northeastern University', 'South Station', 'Theatre District', 'West End'])

destination = st.sidebar.selectbox('Destination', ['Back Bay', 'Beacon Hill', 'Boston University', 'Fenway', 'Financial District', 'Haymarket Square', 'North End', 'North Station', 'Northeastern University', 'South Station', 'Theatre District', 'West End'])
cab_type = st.sidebar.selectbox('cab_type',['Uber','Lyft'])
name = st.sidebar.selectbox('name',['Black', 'Black SUV', 'Lux','Lux Black', 'Lux Black XL', 'Lyft', 'Lyft XL', 'Shared','UberPool','UberX', 'UberXL', 'WAV'])
icon = st.sidebar.selectbox('icon',['clear-day','clear-night', 'cloudy', 'fog', 'partly-cloudy-day','partly-cloudy-night', 'rain'])

# Convert source to one-hot encoding
source_cols = ['source_Back Bay', 'source_Beacon Hill', 'source_Boston University', 'source_Fenway', 'source_Financial District', 'source_Haymarket Square','source_North End', 'source_North Station', 'source_Northeastern University','source_South Station', 
'source_Theatre District', 'source_West End'] 
                            
source_dict = dict(zip(source_cols, [0]*len(source_cols)))
source_dict['source_'+source] = 1
destination_cols = ['destination_Back Bay', 'destination_Beacon Hill', 'destination_Boston University', 'destination_Fenway',                                  'destination_Financial District', 'destination_Haymarket Square', 'destination_North End', 'destination_North Station',                      'destination_Northeastern University', 'destination_South Station', 'destination_Theatre District', 
                   'destination_West End']
                            
destination_dict = dict(zip(destination_cols, [0]*len(destination_cols)))
destination_dict['destination_'+destination] = 1

cab_type_cols = ['cab_type_Lyft', 'cab_type_Uber']
cab_type_dict = dict(zip(cab_type_cols, [0]*len(cab_type_cols)))
cab_type_dict['cab_type_'+cab_type] = 1
name_cols = ['name_Black', 'name_Black SUV', 'name_Lux',
            'name_Lux Black', 'name_Lux Black XL', 'name_Lyft', 'name_Lyft XL', 'name_Shared',
            'name_UberPool', 'name_UberX', 'name_UberXL', 'name_WAV']
name_dict = dict(zip(name_cols, [0]*len(name_cols)))
name_dict['name_'+name] = 1

icon_cols = ['icon_clear-day','icon_clear-night', 'icon_cloudy', 'icon_fog', 'icon_partly-cloudy-day',
             'icon_partly-cloudy-night','icon_rain']
icon_dict = dict(zip(icon_cols, [0]*len(icon_cols)))
icon_dict['icon_'+icon] = 1

source_df = pd.DataFrame([source_dict,destination_dict,cab_type_dict,name_dict,icon_dict],index=[1,2,3,4,5])

import streamlit as st
from streamlit_folium import folium_static
import folium

# Create a map centered on Boston
m = folium.Map(location=[42.361145, -71.057083], zoom_start=12)

# Add markers for the source and destination locations
source_coords = {
    'Back Bay': [42.350619, -71.087463],
    'Beacon Hill': [42.358630, -71.067580],
    'Boston University': [42.350313, -71.105452],
    'Fenway': [42.346764, -71.097285],
    'Financial District': [42.355024, -71.057910],
    'Haymarket Square': [42.363919, -71.058384],
    'North End': [42.365855, -71.054225],
    'North Station': [42.365648, -71.061316],
    'Northeastern University': [42.339806, -71.089171],
    'South Station': [42.351738, -71.055716],
    'Theatre District': [42.350177, -71.062818],
    'West End': [42.364095, -71.063923]
}
destination_coords = source_coords.copy()

source_lat, source_lon = source_coords[source]
destination_lat, destination_lon = destination_coords[destination]

source_point = (source_lat, source_lon)
destination_point = (destination_lat, destination_lon)

# Calculate the distance between the source and destination in kilometers
dist_km = round(distance.distance(source_point, destination_point).km, 2)

source_marker = folium.Marker(location=source_coords[source], icon=folium.Icon(color='green'))
destination_marker = folium.Marker(location=destination_coords[destination], icon=folium.Icon(color='red'))
m.add_child(source_marker)
m.add_child(destination_marker)

# Show the map
folium_static(m)

# Predict fares for all cab types and get the minimum fare and cab type
input_df = pd.DataFrame({'distance': dist_km},index=[0])
input_df = pd.concat([input_df, source_df], axis=1)



# Define a function to predict the price
def predict_price():
    input_df = pd.DataFrame({'distance': dist_km},index=[0])
    input_df = pd.concat([input_df, source_df], axis=1)
    prediction = model.predict(input_df)
    price_placeholder = st.empty()
    return prediction[0]

# Call the predict_price function on button click
if st.sidebar.button('Predict Price'):
    price = predict_price()
    with st.spinner(text='Predicting price...'):
        st.write(f'<div style="font-size: 28px; font-weight:bold; color: #ffffff;">Total distance is : <span style="color:                  #9ef01a;">{dist_km:.2f} km </span></div>', unsafe_allow_html=True)
        st.write(f'<div style="font-size: 28px; font-weight:bold; color: #ffffff;">Predicted price is : <span style="color:                  #9ef01a;">${price:.2f}</span></div>', unsafe_allow_html=True)
    for i in name_cols:
        name_dict2 = dict(zip(name_cols, [0]*len(name_cols)))
        name_dict2['name_'+i] = 1
        source_df2 = pd.DataFrame([source_dict,destination_dict,cab_type_dict,name_dict2,icon_dict],index=[1,2,3,4,5])
        input_df2 = pd.DataFrame({'distance': dist_km},index=[0])
        input_df2 = pd.concat([input_df2, source_df2], axis=1)
        fare_predictions = model.predict(input_df)
        fare_predictions = pd.Series(fare_predictions, name='fare')
        cab_fares = pd.DataFrame({'cab_type': i, 'fare_prediction': fare_predictions})
        
    

    min_fare = cab_fares['fare_prediction'].min()
    suitable_cab_type = cab_fares[cab_fares['fare_prediction'] == min_fare]['cab_type'].iloc[0]

    # Print recommendation
    st.write(f'<p style="color:white; font-size:28px; font-weight:bold">Based on the distance and locations you entered, we recommend you take a <span style="color: #9ef01a;">{suitable_cab_type.strip("name_")}</span> cab. It will cost you <span style="color: #9ef01a;">${round(min_fare,2)}</span></p>', unsafe_allow_html=True)


        


