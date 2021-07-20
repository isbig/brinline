from flask import Flask, request, abort
import requests

import os

DATABASE_URL = os.getenv('DATABASE_URL')
SECr = os.getenv('SECr')

app = Flask(__name__)

@app.route("/calen", methods=['POST', 'GET'])
def calen():
    # get X-Line-Signature header value
    state = request.headers['X-Goog-Resource-State']
    uri = request.headers['X-Goog-Resource-URI']
    id = request.headers['X-Goog-Channel-ID']
    token = request.headers['X-Goog-Channel-Token']
    return '200'


url = 'https://notify-api.line.me/api/notify'
token = 'keys'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+SECr}
msg = 'Data TMD Ready'
r = requests.post(url, headers=headers, data = {'message':msg})
print(r.text)


@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'


if __name__ == "__main__":
    app.run()