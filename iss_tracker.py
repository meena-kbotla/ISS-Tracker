from flask import Flask, request, jsonify
import requests
import xmltodict
import math
import time
import redis
from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent='iss_tracker')

app = Flask(__name__)

@app.route('/epochs', methods=['GET'])
@app.route('/epochs/<int:epoch>', methods=['GET'])
@app.route('/epochs/<int:epoch>/<extra>', methods=['GET'])
def return_epoch(epoch=None, extra=None):
    '''
    This function outputs the dataset processed in different forms depending on the flask input. It can also output the speed at a requested epoch.

    Args:
        epoch(int): the index of epoch to output
        extra(str): "speed" if speed should be outputted for the requested epoch
        limit(int): the first index of the range of epochs
        offset(int): the last index of the range of epochs

    Returns:
        the_speed(float): the speed of the requested epoch
        epoch(): the data of the requested epoch
        data(): the data within the provided ranges
    '''
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    data = xmltodict.parse(response.content)
    state_vectors = data['ndm']['oem']['body']['segment']['data']['stateVector']

    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)

    if epoch is not None:
        if extra == 'speed':
            xd = float(state_vectors[epoch]['X_DOT']['#text'])
            yd = float(state_vectors[epoch]['Y_DOT']['#text'])
            zd = float(state_vectors[epoch]['Z_DOT']['#text'])
            xs = xd*xd
            ys = yd*yd
            zs = zd*zd
            the_speed = math.sqrt(xs + ys + zs)
            return f"The speed at epoch {epoch} is {the_speed}"
        elif extra == 'locations':
            geoloc = geocoder.reverse((lat, lon), zoom=15, language='en') 
            
        else:
            return state_vectors[epoch]
    elif limit is not None:
        sliced_data = state_vectors[offset:offset + limit]
        return sliced_data
    else:
        return state_vectors


@app.route('/now', methods=['GET'])
def now_data() -> str:
    '''
    This function pulls the current time stamp and returns the data from the epoch closest to "now"
    
    Return:
        now_epoch (str): The data from the epoch closest to "now"
    '''
    response = requests.get(url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    data = xmltodict.parse(response.content)

    now = time.mktime(time.gmtime())
    time_diff = 9999
    closest_index = -1

    state_vectors = data['ndm']['oem']['body']['segment']['data']['stateVector']
    
    for i in range(0, len(state_vectors)):
        time_stamp = state_vectors[i]['EPOCH']
        compare_to = time.mktime(time.strptime(time_stamp, '%Y-%jT%H:%M:%S.%fZ'))
        check_diff = abs(compare_to - now)
        if check_diff < time_diff:
            time_diff = check_diff
            closest_index = i
    
    closest_epoch = state_vectors[closest_index]
    
    xd = float(state_vectors[closest_index]['X_DOT']['#text'])
    yd = float(state_vectors[closest_index]['Y_DOT']['#text'])
    zd = float(state_vectors[closest_index]['Z_DOT']['#text'])
    xs = xd*xd
    ys = yd*yd
    zs = zd*zd
    speed = math.sqrt(xs + ys + zs)

    return f"Closest epoch: {closest_epoch}, Speed: {speed}"

if __name__ == '__main__':
    app.run(debug=True)
