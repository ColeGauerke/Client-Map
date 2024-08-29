from flask import Flask, render_template
import pandas as pd
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
import folium
import time

app = Flask(__name__)

def geocode_address(geolocator, address, retries=10):
    """
    GEOCODE ADRESS
    This function requires a geolocator, address and the number of retries are equal to three.
    The geolocator being used is googleV3, which will turn the given address into a pair of latitude
    and longitudinal coordinates. The geocoder does not always get the proper coordinates on the first try
    therefore the maximum number of retries is set to 10, but this can be adjusted.
    """
    for i in range(retries):
        try:
            return geolocator.geocode(address, timeout=10)
        except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError) as e:
            print(f"Geocoding error for address '{address}': {e}")
            if i < retries - 1:
                time.sleep(2) 
                continue
            else:
                return None
            
@app.route('/')

def index():
    """
    The index serves as the primary flask web controller for this function and reads data from the excel file,
    geocodes the address, and formats each point on the map to correspond to the proper color coded pin.
    """
    df = pd.read_excel('small_client_list.xlsx')
    geolocator = GoogleV3(api_key='YOUR UNIQUE API KEY')
    map = folium.Map(location=[37.0902, -95.7129], zoom_start=5)
    salesman_colors = {
        "Bryan Techel": "darkred",
        "Chris Wirz": "blue",
        "Mike Klauda": "green",
        "Paul Fiereck": "orange",
        "Pete Dunn": "darkpurple"
    }
    client_count = 0
    for idx, row in df.iterrows():
        address = row['address']
        location = geocode_address(geolocator, address, retries=5)
        if location:
            popup_content = (
                f"<b>Client:</b> {row['name']}<br>"
                f"<b>Salesman:</b> {row['salesman']}"
            )
            folium.Marker(
                [location.latitude, location.longitude],
                popup=popup_content,
                icon=folium.Icon(color=salesman_colors.get(row['salesman'], 'black'))
            ).add_to(map)
            client_count += 1
            if client_count % 5 == 0:
                print(f"{client_count} clients processed and uploaded to the site.")
        else:
            print(f"Geocoding failed for address: {address}")

    print(f"Total clients processed: {client_count}")

    """
    The following legend, and title are html elements, which is made possible through the use of folium
    """

    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 200px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
     ">&nbsp; <b>Corresponding Salesman</b> <br>
     &nbsp; <i class="fa fa-map-marker fa-2x" style="color:darkred"></i>&nbsp; Bryan Techel <br>
     &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i>&nbsp; Chris Wirz <br>
     &nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i>&nbsp; Mike Klauda <br>
     &nbsp; <i class="fa fa-map-marker fa-2x" style="color:orange"></i>&nbsp; Paul Fiereck <br>
     &nbsp; <i class="fa fa-map-marker fa-2x" style="color:purple"></i>&nbsp; Pete Dunn <br>
      </div>
     '''
    map.get_root().html.add_child(folium.Element(legend_html))

    title_html = '''
     <div style="position: fixed; 
     bottom: 10px; right: 10px; width: 250px; height: 50px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:16px;
     ">&nbsp; <b>North Central Bus Clients</b> <br>
     &nbsp; <span style="font-size:12px;">Created by Cole Gauerke</span>
     </div>
     '''
    map.get_root().html.add_child(folium.Element(title_html))

    map.save('templates/map.html')
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
