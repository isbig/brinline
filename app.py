from flask import Flask, request, abort
import requests
import time

import os
import patitin as pt
import datetime

DATABASE_URL = os.getenv('DATABASE_URL')
SECr = os.getenv('SECr')

app = Flask(__name__)


def sent_noti_event(token):
    notina = pt.ReadEvent()
    noti = notina.push_noti(token)
    return noti


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
    expiration_time = request.headers['X-Goog-Channel-Expiration']
    token = request.headers['X-Goog-Channel-Token']
    datetime_exp = datetime.datetime.strptime("Tue, 27 Jul 2021 07:26:12 GMT", '%a, %d %b %Y %H:%M:%S %Z')
    datetime_before_exp_2 = datetime_exp - datetime.timedelta(days=2)
    next_exp = datetime_exp + datetime.timedelta(days=30)
    unixtime = time.mktime(next_exp.timetuple())
    unixtime_exp = int(unixtime * 1000)
    if datetime_before_exp_2 < datetime.datetime.now():
        # วันนี้เลย วันครบกำหนดลบ2 มาแล้ว ให้ทำการต่ออายุ
        notina = pt.GetItem()
        address = "https://brinline.herokuapp.com/calen"
        name_cal = token
        toayu = notina.watch(address, name_cal, str(unixtime_exp))
    else:
        # วันนี้ยังไม่ถึง วันครบกำหนดลบ2 มาแล้ว ให้ทำการต่ออายุ
        pass
    print(token)
    print(expiration_time)
    sent_notify(token)
    return '200'


@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'


if __name__ == "__main__":
    app.run()