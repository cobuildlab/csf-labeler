from wifi import Cell, Scheme
############ credentials from txt #######################
with open('creds.txt', 'r') as myfile:
    mycreds = myfile.read().split()
myssid = mycreds[0]
mypass = mycreds[1]
#########################################################
allSSID = [cell.ssid for cell in Cell.all('wlan0')]
if myssid in allSSID:
    print(myssid + ' found!')
    file = open("/etc/wpa_supplicant/wpa_supplicant.conf","w")
    file.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n\n')
    file.write('update_config=1\n\n'+'country=US\n\n')
    file.write('network={\n'+'ssid="'+ myssid +'"\n')
    file.write('psk="'+ mypass +'"\n'+'key_mgmt=WPA-PSK\n'+'}')
    file.close()
else:
    print(myssid + ' not found') 