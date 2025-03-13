from flask import Flask, request, jsonify
import requests
import xmltodict
import math

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

    input_limit = request.args.get('limit', type=int)
    input_offset = request.args.get('offset', type=int)

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
        else:
            return state_vectors[epoch]
    elif input_limit is not None and input_offset is not None:
        while i in range (0, input_limit):
            return jsonify(state_vectors[input_offset + i])
    else:
        return f"Haha"

if __name__ == '__main__':
    app.run(debug=True)
