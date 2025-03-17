from iss_tracker import return_epoch
from iss_tracker import now_data

data = {
    'ndm': {
        'oem': {
            'body': {
                'segment': {
                    'data': {  # Added this 'data' key to match the access path
                        'stateVector': [
                            {
                                'EPOCH': '2025-048T12:00:00.000Z',
                                'X_DOT': {'#text': -7.4279612527938603},
                                'Y_DOT': {'#text': -1.0957184455411599},
                                'Z_DOT': {'#text': 1.48575598628449}
                            },
                            {
                                'EPOCH': '2025-048T12:04:00.000Z',
                                'X_DOT': {'#text': -6.6672197179061703},
                                'Y_DOT': {'#text': -2.2893264279998999},
                                'Z_DOT': {'#text': 2.9866174446820102}
                            },
                            {
                                'EPOCH': '2025-048T12:08:00.000Z',
                                'X_DOT': {'#text': -5.4213681121717698},
                                'Y_DOT': {'#text': -3.31822440154414},
                                'Z_DOT': {'#text': 4.2719339962098202}
                            }
                        ]
                    }
                }
            }
        }
    }
}

BASE_URL = "http://localhost:5000/epochs"

def test_epoch_data(epoch):
    url = f"{BASE_URL}/{epoch}"
    response = requests.get(url)
    print(response.text)

def test_speed_data(epoch):
    url = f"{BASE_URL}/{epoch}/speed"
    response = requests.get(url)
    print(response.text)

def test_range_data(limit, offset):
    url = f"{BASE_URL}?limit={limit}&offset={offset}"
    response = requests.get(url)
    print(response.text)

test_epoch_data(99)
test_speed_data(99)
test_range_data(0, 99)

def test_now_data(now)
    url = f"http://localhost:5000/now"

test_now_data()
