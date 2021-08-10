import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import random
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

def elevation_profile():
        print()


elevation_map(lat = 40.831163123486064,
              long = 9.069893611397163,
              radius = 10,
              resolution = 0.5)