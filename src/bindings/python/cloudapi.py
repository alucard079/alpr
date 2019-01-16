import requests
import base64
import json

# Sample image file is available at http://plates.openalpr.com/ea7the.jpg
IMAGE_PATH = 'lp5.jpg'
SECRET_KEY = 'sk_339983d56c44ca5bbb216fe9'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=0&country=eu&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)
a = json.dumps(r.json())
x = 'CM4741'
data = json.loads(a)
app = ''
for plate in data['results']:
    if x == plate['plate']:
        app += plate['plate'] + ' matched'
        print(json.dumps(r.json(), indent=2))
    else :
        app += plate['plate'] + ' not matched'
        print(json.dumps(r.json(), indent=2))

print (app)
