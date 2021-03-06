import json
import sqlite3
import sys 

db = sqlite3.connect('survey.sqlite')
cursor = db.cursor()

#Create table
cursor.execute('''
    CREATE TABLE survey(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        long TEXT NOT NULL, 
                        lat TEXT NOT NULL,
                        status TEXT NOT NULL,
                        street TEXT NOT NULL, 
                        housenumber TEXT NOT NULL)
''')

# Load OSM
with open('osm_data.geojson') as f:
  osm_data = json.load(f)
  
  
# Iterate through all features of GEOJSON
for feature in osm_data['features']:
        geometry = feature['geometry']
        lat_arr = []
        long_arr = []
        
        # Get center of coordinates for marker
        if isinstance(geometry['coordinates'][0], list):
            for coord in geometry['coordinates'][0]:
                lat_arr.append(coord[1])
                long_arr.append(coord[0])
                
            lat = sum(lat_arr)/len(lat_arr)
            long = sum(long_arr)/len(long_arr)    
        else:
            lat = geometry['coordinates'][1]
            long = geometry['coordinates'][0] 


        status = "unknown"
        street = feature['properties']['addr:street']

        # Skip if no house number exists
        if feature['properties'].get('addr:housenumber') is None:
            continue
        housenumber = feature['properties']['addr:housenumber']
        
        # Add to database
        cursor.execute('''INSERT INTO survey(long, lat, status, street, housenumber)
                            VALUES(?,?,?,?,?,?)''', (long, lat, status, street, housenumber))
                                           
db.commit()