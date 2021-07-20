from flask import Flask, request, abort
import requests

import os
import patitin as pt

DATABASE_URL = os.getenv('DATABASE_URL')
SECr = os.getenv('SECr')

app = Flask(__name__)


def sent_noti_event(token):
    notina = pt.ReadEvent()
    noti = notina.push_noti(token)
    out_me = noti.push_noti(token)
    return out_me


def sent_notify(token_cal):
    url = 'https://notify-api.line.me/api/notify'
    token = 'keys'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+SECr}
    msg = sent_noti_event(token_cal)
    r = requests.post(url, headers=headers, data = {'message':msg})


@app.route("/calen", methods=['POST', 'GET'])
def calen():
    # get X-Line-Signature header value
    state = request.headers['X-Goog-Resource-State']
    uri = request.headers['X-Goog-Resource-URI']
    id = request.headers['X-Goog-Channel-ID']
    token = request.headers['X-Goog-Channel-Token']
    print(token)
    sent_notify(token)
    return '200'


@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'


if __name__ == "__main__":
    app.run()