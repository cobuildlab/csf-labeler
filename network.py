import urllib


def check_network_conn():
    try:
        urllib.request.urlopen('https://csfcouriersltd.com')
        return True
    except:
        return False