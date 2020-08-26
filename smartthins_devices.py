import requests
import json
import sys

if len(sys.argv) < 2:
    print('smartthings token이 입력되지 않았습니다.')
    sys.exit()

token = sys.argv[1]

SMARTTHINGS_API_URL = 'https://api.smartthings.com/v1/devices'

headers = {
    'Authorization' : 'Bearer {}'.format(token)
}

url = SMARTTHINGS_API_URL

response = requests.get(url, headers = headers)

rescode = response.status_code

print(f'status_code : {rescode}')

if ( rescode == 200 ):
    response_body = response.content
else:
    print(f'Error Code: {rescode}')
    sys.exit()

items = response.json()['items']

devices = {}

for i in items:
    print('[device info] -------------------------------------')
    print('+ Device ID : {}'.format(i['deviceId']))
    print('+ Name      : {}'.format(i['name']))
    print('+ Label     : {}'.format(i['label']))
    components = i['components']
    for c in components:
        print( '[ {} ]'.format( str(c['id'])) )
        capa = c['capabilities']

        for cp in capa:
            print('|- {} / ver.{}'.format(str(cp['id']), str(cp['version']))  )
print('-------------------------------------------------')
