import time
import unittest
import uuid
import requests

from network import check_network_conn, RequestSender


class NetworkTestCase(unittest.TestCase):
    def test_is_connected(self):
        result = check_network_conn()
        self.assertEqual(result, True)

    def test_unreachable(self):
        url = 'asdfasdf.csda'
        result = check_network_conn(url=url)
        self.assertEqual(result, False)

    def test_post_data(self):
        unique_id = str(uuid.uuid4())
        scanned_code = f'TEST-SCANNED-CODE-{time.time()}'
        rounded_weight = '0.5'
        request_sender = RequestSender(unique_id, scanned_code, rounded_weight)
        request_sender.run()

    def test_error_post_data(self):
        unique_id = str(uuid.uuid4())
        scanned_code = 'TEST-SCANNED-CODE'
        rounded_weight = '0.5'
        request_sender = RequestSender(unique_id, scanned_code, rounded_weight)

        with self.assertRaises(requests.exceptions.ConnectTimeout):
            request_sender.run(url='https://some.unreachable.url/test')


if __name__ == '__main__':
    unittest.main()
