import urllib


def check_network_conn():
    try:
        urllib.request.urlopen('https://google.com')
        return True
    except:
        return False