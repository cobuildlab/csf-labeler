import urllib
from threading import Thread

import requests


def check_network_conn():
    try:
        urllib.request.urlopen('https://csfcouriersltd.com')
        return True
    except Exception as e:
        return False


class RequestSender(Thread):
    def __init__(self, unique_id, scanned_code, rounded_weight):
        Thread.__init__(self)
        self.unique_id = unique_id
        self.scanned_code = scanned_code
        self.rounded_weight = rounded_weight

    def run(self):
        print("RequestSender:run:", self.unique_id, self.scanned_code, self.rounded_weight)

        url = "https://csfcouriersltd.com/ws/weighted_package"
        print("RequestSender:run:rounded_weight:url", url)
        request_data = {"receipt_number": self.scanned_code, "packageId": self.unique_id,
                        "weight": self.rounded_weight,
                        "username": "csfcourierltd", "password": "6Ld9y1saAAAAAFY5xdTG3bCjZ7jCnfhqztPdXKUL"}
        print("RequestSender:run:request_data:", request_data)
        try:
            response = requests.post(url, data=request_data)
            print("RequestSender:run:response:", response.text)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("RequestSender:run:error: Something goes wrong", e)
