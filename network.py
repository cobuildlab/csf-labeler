import http.client as httplib
from threading import Thread
import requests

HOST_URL = 'csfcouriersltd.com'
POST_ALERT_URL = "https://csfcouriersltd.com/ws/weighted_package"


def check_network_conn(url=HOST_URL):
    conn = httplib.HTTPSConnection(url, timeout=3)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception as e:
        return False
    finally:
        conn.close()


class RequestSender(Thread):
    def __init__(self, unique_id, scanned_code, rounded_weight):
        Thread.__init__(self, name="RequestSender")
        self.unique_id = unique_id
        self.scanned_code = scanned_code
        self.rounded_weight = rounded_weight

    def run(self, url=POST_ALERT_URL):
        print("RequestSender:run:", self.unique_id, self.scanned_code, self.rounded_weight)
        print("RequestSender:run:rounded_weight:url", url)
        request_data = {"receipt_number": self.scanned_code, "packageId": self.unique_id,
                        "weight": self.rounded_weight,
                        "username": "csfcourierltd", "password": "6Ld9y1saAAAAAFY5xdTG3bCjZ7jCnfhqztPdXKUL"}
        print("RequestSender:run:request_data:", request_data)

        try:
            response = requests.post(url, data=request_data, timeout=3)
            print("RequestSender:run:response:", response.text)
        except requests.exceptions.ConnectTimeout as e:
            print("RequestSender:run:error: Connection timeout", e)
            raise e
        except Exception as e:
            print("RequestSender:run:error: Something went wrong", e)
            raise e
