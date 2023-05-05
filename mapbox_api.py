import requests
import csv
import numpy as np
from tqdm import tqdm

def mapbox_request(pcd, long, lat):
    url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{long},{lat},15,0,0/600x600?access_token=INSERT_KEY_HERE"
    response = requests.get(url)
    
    pic_path = f"pic_{pcd}_sat.jpg"

    if response.status_code == 200:
        with open(pic_path, 'wb') as f:
            f.write(response.content)


with open("dataset.csv",'r') as dest_f:
    data_iter = csv.reader(dest_f, delimiter = ',')
    data = [data for data in data_iter]
data_array = np.asarray(data, dtype=str)

pcd_array = data_array.T[5][1:]
lat_array = data_array.T[7][1:]
long_array = data_array.T[8][1:]

for i, pcd in enumerate(tqdm(pcd_array)):
    mapbox_request(pcd, long_array[i], lat_array[i])