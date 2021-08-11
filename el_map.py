import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import math
from time import sleep

class colors:
        reset='\033[0m'
        bold='\033[01m'
        disable='\033[02m'
        underline='\033[04m'
        reverse='\033[07m'
        strikethrough='\033[09m'
        invisible='\033[08m'
        class fg:
                black='\033[30m'
                red='\033[31m'
                green='\033[32m'
                orange='\033[33m'
                blue='\033[34m'
                purple='\033[35m'
                cyan='\033[36m'
                lightgrey='\033[37m'
                darkgrey='\033[90m'
                lightred='\033[91m'
                lightgreen='\033[92m'
                yellow='\033[93m'
                lightblue='\033[94m'
                pink='\033[95m'
                lightcyan='\033[96m'
        class bg:
                black='\033[40m'
                red='\033[41m'
                green='\033[42m'
                orange='\033[43m'
                blue='\033[44m'
                purple='\033[45m'
                cyan='\033[46m'
                lightgrey='\033[47m'
 
def update_progress(progress):
        print('\r{0} |{1}{2}| {3}%'.format('Progress:', '█'*int(progress/5), ' '*int(20 - int(progress/5)), round(progress, 2)), end='')

def elevation_map(lat, long, radius, resolution):
        # Tx location [lat, long]
        Tx = [lat, long]

        # Get list of locations
        locations = ""

        for lat in np.arange(Tx[0]-radius/2, Tx[0]+radius/2, resolution):
                for long in np.arange(Tx[1]-radius/2, Tx[1]+radius/2, resolution):
                        locations = locations + str(lat)+","+str(long)+"|"

        # Delete trailing "|" separator
        locations = locations[:-1]

        # Fetch elevations
        dataset = 'EU-DEM (25m)'
        print('Fetching elevation data from '+colors.bold+dataset+colors.reset+'...')
        url = "https://api.opentopodata.org/v1/eudem25m?"

        heatmap = np.array([])
        locations100 = ""
        i = 0
        for location in locations.split("|"):
                locations100 = locations100 + location + "|"
                i += 1
                if i % 100 == 0 or i == len(locations.split("|")):
                        locations100 = locations100[:-1]
                        #print(locations100) #print set
                        data = "locations="+locations100
                        response = requests.get(url, data, headers={'content-type': 'application/json'})
                        # Parse response to json
                        response = response.json()
                        for j in range (0, len(response['results'])):
                                elevation = response['results'][j]['elevation']
                                if elevation == 'null' or elevation is None:
                                        elevation = np.nan
                                else:
                                        elevation = float(elevation)
                                #print(elevation)
                                heatmap = np.append(heatmap, elevation)
                        locations100 = ""
                        update_progress(100*i/len(locations.split("|")))
        print()

        heatmap = heatmap.reshape(-1, len(np.arange(Tx[0]-radius/2, Tx[0]+radius/2, resolution)))
        heatmap = np.flipud(heatmap)
        plt.imshow(heatmap, interpolation='gaussian', extent=[
                np.min(np.arange(Tx[1]-radius/2, Tx[1]+radius/2, resolution)),
                np.max(np.arange(Tx[1]-radius/2, Tx[1]+radius/2, resolution)),
                np.min(np.arange(Tx[0]-radius/2, Tx[0]+radius/2, resolution)),
                np.max(np.arange(Tx[0]-radius/2, Tx[0]+radius/2, resolution))
                ])
        plt.show()

def elevation_profile(lat_start, long_start, lat_end, long_end, pts=200):
        #START-END POINT
        P1=[lat_start, long_start]
        P2=[lat_end, long_end]
        #NUMBER OF POINTS
        pts -= 1
        interval_lat=(P2[0]-P1[0])/pts #interval for latitude
        interval_lon=(P2[1]-P1[1])/pts #interval for longitude
        #SET A NEW VARIABLE FOR START POINT
        lat0=P1[0]
        lon0=P1[1]
        #LATITUDE AND LONGITUDE LIST
        lat_list=[lat0]
        lon_list=[lon0]
        #GENERATING POINTS
        for i in range(pts):
                lat_step=lat0+interval_lat
                lon_step=lon0+interval_lon
                lon0=lon_step
                lat0=lat_step
                lat_list.append(lat_step)
                lon_list.append(lon_step)
        #HAVERSINE FUNCTION
        def haversine(lat1,lon1,lat2,lon2):
                lat1_rad=math.radians(lat1)
                lat2_rad=math.radians(lat2)
                lon1_rad=math.radians(lon1)
                lon2_rad=math.radians(lon2)
                delta_lat=lat2_rad-lat1_rad
                delta_lon=lon2_rad-lon1_rad
                a=math.sqrt((math.sin(delta_lat/2))**2+math.cos(lat1_rad)*math.cos(lat2_rad)*(math.sin(delta_lon/2))**2)
                d=2*6371000*math.asin(a)
                return d
        #DISTANCE CALCULATION
        d_list=[]
        for j in range(len(lat_list)):
                lat_p=lat_list[j]
                lon_p=lon_list[j]
                dp=haversine(lat0,lon0,lat_p,lon_p)/1000 #km
                d_list.append(dp)
        d_list_rev=d_list[::-1] #reverse list
        #CONSTRUCT JSON
        #d_ar=[{}]*len(lat_list)
        #for i in range(len(lat_list)):
        #        d_ar[i]={"latitude":lat_list[i],"longitude":lon_list[i]}
        locations = ""
        for i in range(len(lat_list)):
                locations = locations + str(lat_list[i])+","+str(lon_list[i])+"|"
        # Delete trailing "|" separator
        locations = locations[:-1]
        data = "locations="+locations
        #location={"locations":d_ar}
        #print(location)
        json_data=json.dumps(locations,skipkeys=int).encode('utf8')
        #print(json_data)
        dataset = 'EU-DEM (25m)'
        print('Fetching elevation data from '+colors.bold+dataset+colors.reset+'...')
        url="https://api.opentopodata.org/v1/eudem25m?"
        ###response = urllib.request.Request(url,json_data,headers={'Content-Type': 'application/json'})
        response = requests.get(url, data, headers={'content-type': 'application/json'})
        # Parse response to json
        response = response.json()
        elev_list=[]
        locations100 = ""
        i = 0
        for location in locations.split("|"):
                locations100 = locations100 + location + "|"
                i += 1
                if i % 100 == 0 or i == len(locations.split("|")):
                        locations100 = locations100[:-1]
                        #print(locations100) #print set
                        data = "locations="+locations100
                        response = requests.get(url, data, headers={'content-type': 'application/json'})
                        # Parse response to json
                        response = response.json()
                        for j in range (0, len(response['results'])):
                                elevation = response['results'][j]['elevation']
                                if elevation == 'null' or elevation is None:
                                        elevation = np.nan
                                else:
                                        elevation = float(elevation)
                                elev_list.append(elevation)
                        locations100 = ""
                        update_progress(100*i/len(locations.split("|")))
        print()

        #BASIC STAT INFORMATION
        mean_elev=round((sum(elev_list)/len(elev_list)),3)
        min_elev=min(elev_list)
        max_elev=max(elev_list)
        distance=d_list_rev[-1]

        #PLOT ELEVATION PROFILE
        base_reg=0
        plt.figure(figsize=(10,4))
        plt.plot(d_list_rev,elev_list)
        plt.plot([0,distance],[min_elev,min_elev],'--g',label='min: '+str(min_elev)+' m')
        plt.plot([0,distance],[max_elev,max_elev],'--r',label='max: '+str(max_elev)+' m')
        plt.plot([0,distance],[mean_elev,mean_elev],'--y',label='ave: '+str(mean_elev)+' m')
        plt.fill_between(d_list_rev,elev_list,base_reg,alpha=0.1)
        plt.text(d_list_rev[0],elev_list[0],"P1")
        plt.text(d_list_rev[-1],elev_list[-1],"P2")
        plt.xlabel("Distance(km)")
        plt.ylabel("Elevation(m)")
        plt.grid()
        plt.legend(fontsize='small')
        plt.show()

elevation_map(lat = 40.831163123486064,
              long = 9.069893611397163,
              radius = 10,
              resolution = 0.5)

elevation_profile(lat_start=37.92004381769315,
                  long_start=20.6882094302896,
                  lat_end=37.92004381769315,
                  long_end=20.6982094302896,
                  pts=205)