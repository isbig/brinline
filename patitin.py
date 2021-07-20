from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from pythainlp.util import thai_strftime
import uuid
import os
from pytz import timezone
import psycopg2
from psycopg2.extras import Json, DictCursor

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError:
    import keyda as kd
    DATABASE_URL = kd.DATABASE_URL

class WithDatabase:
    def __init__(self, database_url):
        self.conn = psycopg2.connect(database_url, sslmode='require')
        self.cur = self.conn.cursor(cursor_factory=DictCursor)

    def find(self, date):
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM bigger_data WHERE date = date %(date)s);", {'date': date})
        row = self.cur.fetchall()
        return row

    def insert_date(self, date):
        if self.find(date) == [[False]]:
            self.cur.execute('INSERT INTO bigger_data (date) VALUES (date %(date)s);', {'date': date})
            self.conn.commit()
            print('เพิ่มวันที่นี้ {} ลงในฐานข้อมูลได้สำเร็จ'.format(str(date)))
        else:
            print("วันนี้มีอยู่แล้ว")

    def insert_sync(self, date, sync):
        if self.find(date) == [[False]]:
            self.cur.execute('INSERT INTO bigger_data (date) VALUES (date %(date)s);', {'date': date})
            self.conn.commit()
            print('เพิ่มวันที่นี้ {} ลงในฐานข้อมูลได้สำเร็จ'.format(str(date)))
        else:
            print("วันนี้มีอยู่แล้ว")

    def insert_syncToken_orthcal(self, date, syncToken):
        self.insert_date(date)
        self.cur.execute('SELECT sync_token_orthcal FROM bigger_data where date = date %(date)s;', {'date': date})
        old_data = self.cur.fetchall()
        if old_data == [[None]]:
            new_el = Json([syncToken])
            self.cur.execute(
                "UPDATE bigger_data SET sync_token_orthcal = %(syncToken)s WHERE date = date %(date)s;",
                {'syncToken': new_el, 'date': date})
            self.conn.commit()
        else:
            new_el = old_data[0][0]
            if syncToken not in new_el:
                new_el.append(syncToken)
                print(new_el)
                new_el = Json(new_el)
                self.cur.execute(
                    "UPDATE bigger_data SET sync_token_orthcal = %(syncToken)s WHERE date = date %(date)s;",
                    {'syncToken': new_el, 'date': date})
                self.conn.commit()
                print('เพิ่มข้อมูลใหม่เข้าท้ายลิสต์สำเร็จ')
            else:
                print('ค่านี้มีอยู่แล้ว')

    def insert_syncToken_gpcal(self, date, syncToken):
        self.insert_date(date)
        self.cur.execute('SELECT sync_token_gpcal FROM bigger_data where date = date %(date)s;', {'date': date})
        old_data = self.cur.fetchall()
        if old_data == [[None]]:
            new_el = Json([syncToken])
            self.cur.execute(
                "UPDATE bigger_data SET sync_token_gpcal = %(syncToken)s WHERE date = date %(date)s;",
                {'syncToken': new_el, 'date': date})
            self.conn.commit()
        else:
            new_el = old_data[0][0]
            if syncToken not in new_el:
                new_el.append(syncToken)
                new_el = Json(new_el)
                self.cur.execute(
                    "UPDATE bigger_data SET sync_token_gpcal = %(syncToken)s WHERE date = date %(date)s;",
                    {'syncToken': new_el, 'date': date})
                self.conn.commit()
                print('เพิ่มข้อมูลใหม่เข้าท้ายลิสต์สำเร็จ')
            else:
                print('ค่านี้มีอยู่แล้ว')

    def insert_syncToken_dtcal(self, date, syncToken):
        self.insert_date(date)
        self.cur.execute('SELECT sync_token_dtcal FROM bigger_data where date = date %(date)s;', {'date': date})
        old_data = self.cur.fetchall()
        if old_data == [[None]]:
            new_el = Json([syncToken])
            self.cur.execute(
                "UPDATE bigger_data SET sync_token_dtcal = %(syncToken)s WHERE date = date %(date)s;",
                {'syncToken': new_el, 'date': date})
            self.conn.commit()
        else:
            new_el = old_data[0][0]
            if syncToken not in new_el:
                new_el.append(syncToken)
                new_el = Json(new_el)
                self.cur.execute(
                    "UPDATE bigger_data SET sync_token_dtcal = %(syncToken)s WHERE date = date %(date)s;",
                    {'syncToken': new_el, 'date': date})
                self.conn.commit()
                print('เพิ่มข้อมูลใหม่เข้าท้ายลิสต์สำเร็จ')
            else:
                print('ค่านี้มีอยู่แล้ว')

    def insert_syncToken_ascal(self, date, syncToken):
        self.insert_date(date)
        self.cur.execute('SELECT sync_token_ascal FROM bigger_data where date = date %(date)s;', {'date': date})
        old_data = self.cur.fetchall()
        if old_data == [[None]]:
            new_el = Json([syncToken])
            self.cur.execute(
                "UPDATE bigger_data SET sync_token_ascal = %(syncToken)s WHERE date = date %(date)s;",
                {'syncToken': new_el, 'date': date})
            self.conn.commit()
        else:
            new_el = old_data[0][0]
            if syncToken not in new_el:
                new_el.append(syncToken)
                new_el = Json(new_el)
                self.cur.execute(
                    "UPDATE bigger_data SET sync_token_ascal = %(syncToken)s WHERE date = date %(date)s;",
                    {'syncToken': new_el, 'date': date})
                self.conn.commit()
                print('เพิ่มข้อมูลใหม่เข้าท้ายลิสต์สำเร็จ')
            else:
                print('ค่านี้มีอยู่แล้ว')

    def insert_syncToken_comcal(self, date, syncToken):
        self.insert_date(date)
        self.cur.execute('SELECT sync_token_comcal FROM bigger_data where date = date %(date)s;', {'date': date})
        old_data = self.cur.fetchall()
        if old_data == [[None]]:
            new_el = Json([syncToken])
            self.cur.execute(
                "UPDATE bigger_data SET sync_token_comcal = %(syncToken)s WHERE date = date %(date)s;",
                {'syncToken': new_el, 'date': date})
            self.conn.commit()
        else:
            new_el = old_data[0][0]
            if syncToken not in new_el:
                new_el.append(syncToken)
                new_el = Json(new_el)
                self.cur.execute(
                    "UPDATE bigger_data SET sync_token_comcal = %(syncToken)s WHERE date = date %(date)s;",
                    {'syncToken': new_el, 'date': date})
                self.conn.commit()
                print('เพิ่มข้อมูลใหม่เข้าท้ายลิสต์สำเร็จ')
            else:
                print('ค่านี้มีอยู่แล้ว')

    def insert_syncToken_unconcal(self, date, syncToken):
        self.insert_date(date)
        self.cur.execute('SELECT sync_token_unconcal FROM bigger_data where date = date %(date)s;', {'date': date})
        old_data = self.cur.fetchall()
        if old_data == [[None]]:
            new_el = Json([syncToken])
            self.cur.execute(
                "UPDATE bigger_data SET sync_token_unconcal = %(syncToken)s WHERE date = date %(date)s;",
                {'syncToken': new_el, 'date': date})
            self.conn.commit()
        else:
            new_el = old_data[0][0]
            if syncToken not in new_el:
                new_el.append(syncToken)
                new_el = Json(new_el)
                self.cur.execute(
                    "UPDATE bigger_data SET sync_token_unconcal = %(syncToken)s WHERE date = date %(date)s;",
                    {'syncToken': new_el, 'date': date})
                self.conn.commit()
                print('เพิ่มข้อมูลใหม่เข้าท้ายลิสต์สำเร็จ')
            else:
                print('ค่านี้มีอยู่แล้ว')

    def insert_syncToken_delcal(self, date, syncToken):
        self.insert_date(date)
        self.cur.execute('SELECT sync_token_delcal FROM bigger_data where date = date %(date)s;', {'date': date})
        old_data = self.cur.fetchall()
        if old_data == [[None]]:
            new_el = Json([syncToken])
            self.cur.execute(
                "UPDATE bigger_data SET sync_token_delcal = %(syncToken)s WHERE date = date %(date)s;",
                {'syncToken': new_el, 'date': date})
            self.conn.commit()
        else:
            new_el = old_data[0][0]
            if syncToken not in new_el:
                new_el.append(syncToken)
                new_el = Json(new_el)
                self.cur.execute(
                    "UPDATE bigger_data SET sync_token_delcal = %(syncToken)s WHERE date = date %(date)s;",
                    {'syncToken': new_el, 'date': date})
                self.conn.commit()
                print('เพิ่มข้อมูลใหม่เข้าท้ายลิสต์สำเร็จ')
            else:
                print('ค่านี้มีอยู่แล้ว')

    def last_token_orthcal(self):
        self.cur.execute(
            'SELECT DISTINCT ON ("sync_token_orthcal") * FROM "bigger_data" ORDER  BY "sync_token_orthcal", "date" DESC NULLS LAST, "sync_token_orthcal";')
        old_data = self.cur.fetchone()
        return old_data[1][-1]

    def last_token_gpcal(self):
        self.cur.execute(
            'SELECT DISTINCT ON ("sync_token_gpcal") * FROM "bigger_data" ORDER  BY "sync_token_gpcal", "date" DESC NULLS LAST, "sync_token_gpcal";')
        old_data = self.cur.fetchone()
        return old_data[2][-1]

    def last_token_dtcal(self):
        self.cur.execute(
            'SELECT DISTINCT ON ("sync_token_dtcal") * FROM "bigger_data" ORDER  BY "sync_token_dtcal", "date" DESC NULLS LAST, "sync_token_dtcal";')
        old_data = self.cur.fetchone()
        return old_data[3][-1]

    def last_token_ascal(self):
        self.cur.execute(
            'SELECT DISTINCT ON ("sync_token_ascal") * FROM "bigger_data" ORDER  BY "sync_token_ascal", "date" DESC NULLS LAST, "sync_token_ascal";')
        old_data = self.cur.fetchone()
        return old_data[4][-1]

    def last_token_comcal(self):
        self.cur.execute(
            'SELECT DISTINCT ON ("sync_token_comcal") * FROM "bigger_data" ORDER  BY "sync_token_comcal", "date" DESC NULLS LAST, "sync_token_comcal";')
        old_data = self.cur.fetchone()
        return old_data[5][-1]

    def last_token_unconcal(self):
        self.cur.execute(
            'SELECT DISTINCT ON ("sync_token_unconcal") * FROM "bigger_data" ORDER  BY "sync_token_unconcal", "date" DESC NULLS LAST, "sync_token_unconcal";')
        old_data = self.cur.fetchone()
        return old_data[6][-1]

    def last_token_delcal(self):
        self.cur.execute(
            'SELECT DISTINCT ON ("sync_token_delcal") * FROM "bigger_data" ORDER  BY "sync_token_delcal", "date" DESC NULLS LAST, "sync_token_delcal";')
        old_data = self.cur.fetchone()
        return old_data[7][-1]

    def insert_token_new(self, date, name_cal, syncToken):
        if name_cal == 'orthcal':
            self.insert_syncToken_orthcal(date, syncToken)
        elif name_cal == 'gpcal':
            self.insert_syncToken_gpcal(date, syncToken)
        elif name_cal == 'dtcal':
            self.insert_syncToken_dtcal(date, syncToken)
        elif name_cal == 'ascal':
            self.insert_syncToken_ascal(date, syncToken)
        elif name_cal == 'comcal':
            self.insert_syncToken_comcal(date, syncToken)
        elif name_cal == 'unconcal':
            self.insert_syncToken_unconcal(date, syncToken)
        elif name_cal == 'delcal':
            self.insert_syncToken_delcal(date, syncToken)
        else:
            print("ไม่พบปฏิทินนี้")

    def get_last_token(self, name_cal):
        token = ''
        if name_cal == 'orthcal':
            token = self.last_token_orthcal()
        elif name_cal == 'gpcal':
            token = self.last_token_gpcal()
        elif name_cal == 'dtcal':
            token = self.last_token_dtcal()
        elif name_cal == 'ascal':
            token = self.last_token_ascal()
        elif name_cal == 'comcal':
            token = self.last_token_comcal()
        elif name_cal == 'unconcal':
            token = self.last_token_unconcal()
        elif name_cal == 'delcal':
            token = self.last_token_delcal()
        else:
            print("ไม่พบปฏิทินนี้")
        return token

color_dict = {
    '1': 'ม่วงคราม (ลาเวนเดอร์)',
    '2': 'เขียวอ่อน (สะระแหน่)',
    '3': 'ม่วงชมพู (องุ่น)',
    '4': 'ส้มชมพู (ฟลามิงโก้)',
    '5': 'เหลือง (กล้วย)',
    '6': 'ส้ม (ส้มเขียวหวาน)',
    '7': 'ฟ้า (นกยูง)',
    '8': 'เทา (แกรไฟต์)',
    '9': 'ม่วงน้ำเงิน (บลูเบอร์รี่)',
    '10': 'เขียวเข้ม (โหระพา)',
    '11': 'แดง (มะเขือเทศ)'}
color_code_dict = {
    'undefined': '#039be5',
    '1': '#7986cb',
    '2': '#33b679',
    '3': '#8e24aa',
    '4': '#e67c73',
    '5': '#f6c026',
    '6': '#f5511d',
    '7': '#039be5',
    '8': '#616161',
    '9': '#3f51b5',
    '10': '#0b8043',
    '11': '#d60000)'}


# แปลงเป็นฟอร์แมตแบบไทย
def convert_time_thairead(datetime):
    fmt = "%A %-d/%m/%Y %H:%M"
    return thai_strftime(datetime, fmt)[3:]


# แปลงเป็น datetime เพื่อปรับ timezone ให้เป็นไทย แล้วส่งออกเป็น datetime
def convert_datestring(date_string):
    if date_string[-1] == 'Z':
        date_string = date_string.replace('Z', '+00:00')
    date_time = datetime.datetime.fromisoformat(date_string)
    date_time = date_time.astimezone(timezone('Asia/Bangkok'))
    return date_time

# แปลความจากแต่ละ event ที่ยังเป็น dict
# ไม่ดึงเอา synctoken ออกมาโดยใช้ fuction นี้ ให้ทำข้างนอก
def read_dict_event(obj, *args):
    n = []
    summary_cal = obj.get('summary', [])
    list_of_dict_event = obj.get('items', [])
    if list_of_dict_event:
        for e, item in enumerate(list_of_dict_event):
            item['ลำดับที่'] = str(e + 1)
            item['ปฏิทิน'] = summary_cal
            if item['status'] == "cancelled":
                item['สถานะ'] = "ลบออกจากปฏิทินแล้ว"
            else:
                item['สถานะ'] = "ปรากฏในปฏิทินอยู่"
            item['ลงสี'] = item.get('colorId', 'ไม่ระบุสี')

            createtime = item.get('created', [])
            if createtime:
                item['สร้าง'] = convert_time_thairead(convert_datestring(createtime))
            else:
                item['สร้าง'] = ''
            updatetime = item.get('updated', [])
            if updatetime:
                item['อัพเดต'] = convert_time_thairead(convert_datestring(item['updated']))
            else:
                item['สร้าง'] = ''
            item['นัด'] = item.get('summary', "")
            item['รายละเอียด'] = item.get('description', '')

            creator = item.get('creator', "")
            if creator:
                item['สร้างโดย'] = creator.get('email', '')
            else:
                item['สร้างโดย'] = ""

            organizer = item.get('organizer', "")
            if organizer:
                item['จัดการโดย'] = organizer.get('email', '')
            else:
                item['จัดการโดย'] = ""

            start = item.get('start', "")
            end = item.get('end', "")
            if start and end:
                start_datetime_string = item['start'].get('dateTime', item['start'].get('date'))
                start_datetime = convert_datestring(start_datetime_string)
                item['วันนัด'] = convert_time_thairead(start_datetime)[:-6]

                time_appointment_start = start_datetime.strftime('%H:%M')  # เวลาเริ่มนัดหมาย
                end_time = item['end'].get('dateTime', item['start'].get('date'))
                end_time = convert_datestring(end_time)
                end_time_min = end_time.strftime('%H:%M')  # เวลาสิ้นสุดนัดหมาย
                time_dif = end_time - start_datetime
                minutes_int = int(divmod(time_dif.total_seconds(), 60)[0])

                item['เวลานัด'] = "{}-{} ({} นาที)".format(time_appointment_start, end_time_min, str(minutes_int))
            else:
                item['วันนัด'] = ""
                item['เวลานัด'] = ""
            s = []
            for key in args:
                s.append(key + ": " + item.get(key, ""))
            n.append('\n'.join(s))
    else:
        pass
    return n, list_of_dict_event


# สำหรับรับ object จาก google
class GetItem:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = Credentials.from_authorized_user_file('google-credentials.json', SCOPES)
        self.service = build('calendar', 'v3', credentials=creds)
        self.cal_id = dict(gpcal='johf926ukmc4ebojebk3chk0m4@group.calendar.google.com',
                           orthcal='biggersmile2020@gmail.com',
                           dtcal='j6se8ka1e95iv4cgni31hgnaks@group.calendar.google.com',
                           ascal='5khban1s1eqgl482ojaibe67m0@group.calendar.google.com',
                           comcal='4o21tc0s7scl5e7imubslhabs8@group.calendar.google.com',
                           unconcal='245h7od8qc16r3jtofdth2c1g4@group.calendar.google.com',
                           delcal='34ihuo4qc1r2iijdofq5pjm1a8@group.calendar.google.com')
        self.namecal_dict = {'orthcal': 'เคสจัดฟัน', 'gpcal': 'เคสทั่วไป', 'dtcal': 'หมอ',
                             'ascal': 'ปฏิทินผู้ช่วย', 'comcal': 'ปฏิทินบริษัท', 'unconcal': 'ปฏิทิน เคสเลื่อน',
                             'delcal': 'รายการที่ไม่ใช้'}
        self.showDe = True

    def watch(self, address, name_cal):
        data = {
            "address": address,  # The address where notifications are delivered for this channel.
            "id": str(uuid.uuid4()),  # A UUID or similar unique string that identifies this channel.
            "kind": "api#channel",
            # Identifies this as a notification channel used to watch for changes to a resource, which is "api#channel".
            "type": "web_hook",
            # The type of delivery mechanism used for this channel. Valid values are "web_hook" (or "webhook"). Both
            # values refer to a channel where Http requests are used to deliver messages.
            "token": name_cal
        }
        name_cal = name_cal
        events = self.service.events().watch(calendarId=self.cal_id[name_cal], body=data)
        events.execute()

    def stop_watch(self, address, id_id, resourceId):
        data = {
            "address": address,  # The address where notifications are delivered for this channel.
            "id": id_id,  # A UUID or similar unique string that identifies this channel.
            "resourceId": resourceId
        }
        events = self.service.channels().stop(body=data)
        events.execute()

    def get_one_event(self, name_cal, evenId):
        events = self.service.events().get(calendarId=self.cal_id[name_cal], eventId=evenId)
        events_result = events.execute()
        return events_result

    def search_cal(self, name_cal, text):
        events = self.service.events().list(calendarId=self.cal_id[name_cal], timeMin=None, showDeleted=self.showDe,
                                            singleEvents=True,
                                            orderBy='startTime', q=text)
        events_result = events.execute()
        return events_result

    def get_last(self, day, name_cal):
        date_to = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(
            days=day) - datetime.timedelta(hours=7)
        date_to = date_to.isoformat() + 'Z'
        events = self.service.events().list(calendarId=self.cal_id[name_cal], updatedMin=date_to,
                                            showDeleted=self.showDe, singleEvents=True,
                                            orderBy='updated').execute()
        return events

    def get_onlymod(self, name_cal, syn):
        events = self.service.events().list(calendarId=self.cal_id[name_cal], syncToken=syn).execute()
        item = events.get('items', [])
        new_list_item = []
        if item:
            last_update = datetime.datetime.now() - datetime.timedelta(days=1)
            for event in item:
                updated = event.get('updated', '')
                id_event = event.get('id')
                if updated:
                    updated = datetime.datetime.fromisoformat(updated[:-1])
                else:
                    new_event_data = self.get_one_event(name_cal, id_event)
                    updated = new_event_data.get('updated', '')
                    if updated:
                        updated = datetime.datetime.fromisoformat(updated[:-1])
                        event = new_event_data
                    else:
                        print('ไม่ทราบเวลาอัพเดต')
                if updated > last_update:
                    last_update = updated
                    new_list_item.append(event)
                else:
                    pass
        events['items'] = [new_list_item[-1]]
        return events

    def get_del(self, date, name_cal):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').isoformat() + 'Z'
        events = self.service.events().list(calendarId=self.cal_id[name_cal], timeMin=date, showDeleted=self.showDe,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        return events

    def get_max(self, date, name_cal):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').isoformat() + 'Z'
        events = self.service.events().list(calendarId=self.cal_id[name_cal], timeMin=date, syncToken=None,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        return events

    def get_limit(self, date, day_num, name_cal):
        min_time = datetime.datetime.strptime(date, '%Y-%m-%d') - datetime.timedelta(hours=7)
        min_time = min_time.isoformat() + 'Z'
        max_time = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=day_num) - datetime.timedelta(
            hours=7)
        max_time = max_time.isoformat() + 'Z'
        events = self.service.events().list(calendarId=self.cal_id[name_cal], timeMin=min_time, timeMax=max_time,
                                            singleEvents=True, showDeleted=self.showDe, orderBy='startTime').execute()
        return events

    def get_all(self, date, name_cal):
        list_of_page = []
        date = datetime.datetime.strptime(date, '%Y-%m-%d').isoformat() + 'Z'
        events = self.service.events().list(calendarId=self.cal_id[name_cal], timeMin=date, showDeleted=self.showDe,
                                            singleEvents=True,
                                            orderBy='startTime')
        events_result = events.execute()
        list_of_page.append(events_result)
        while events != None:
            events = self.service.events().list_next(previous_request=events, previous_response=events_result)
            if events != None:
                events_result = events.execute()
            list_of_page.append(events_result)
        return list_of_page

    def get_last_one(self, name_cal):
        date_to = datetime.datetime.now() - datetime.timedelta(
            days=1) - datetime.timedelta(hours=7)
        date_to = date_to.isoformat() + 'Z'
        events = self.service.events().list(calendarId=self.cal_id[name_cal], updatedMin=date_to,
                                            showDeleted=self.showDe, maxResults=1, singleEvents=True,
                                            orderBy='updated').execute()
        return events


def sep_dict_event_by_date(date_string, list_of_new_dict):
    date_want = convert_time_thairead(convert_datestring(date_string))[:-6]
    list_of_same_date_create = []
    list_of_del_event = []
    list_of_puremod = []
    for e, event in enumerate(list_of_new_dict):
        create =  event['created'][:-1]
        update = event['updated'][:-1]
        created = datetime.datetime.fromisoformat(create)
        updated = datetime.datetime.fromisoformat(update)
        duration = updated - created
        duration_in_s = duration.total_seconds()
        # ระยะเวลาระหว่าง สร้างกับ อัพเดต ต่างกันไม่เกิน 60 วิ ให้เป็นการสร้าง เกินกว่านั้นเป็นการอัพเดต
        if event['status'] == 'cancelled':
            list_of_del_event.append(e)
        else:
            if duration_in_s < 60:
                list_of_same_date_create.append(e)
            else:
                list_of_puremod.append(e)
    return [list_of_same_date_create, list_of_del_event, list_of_puremod]


def sepread(object_read, new_list_of_event, date):
    cal_rep = []
    if object_read:
        sep_between_event = "\n____________________________\n"
        date_string = date
        seped = sep_dict_event_by_date(date_string, new_list_of_event)
        cal_rep = ['ปฏิทิน: ' + new_list_of_event[0]['ปฏิทิน']]

        if len(seped[0]) != 0:
            create_date = ['รายการนัดหมายที่ถูก เพิ่มเข้ามา'] + [object_read[x] for x in seped[0]]
            cal_rep.append(sep_between_event.join(create_date))
        if len(seped[1]) != 0:
            deleted_date = ['รายการนัดหมายที่ถูก ลบ'] + [object_read[x] for x in seped[1]]
            cal_rep.append(sep_between_event.join(deleted_date))
        if len(seped[2]) != 0:
            justmod_date = ['รายการนัดหมายที่ถูก แก้ไข'] + [object_read[x] for x in seped[2]]
            cal_rep.append(sep_between_event.join(justmod_date))
        if len(seped[0]) == len(seped[1]) == len(seped[2]) == 0:
            cal_rep = []
    return cal_rep


# สำหรับอ่าน object จาก google
class ReadEvent(GetItem):
    def __init__(self):
        super().__init__()

    # ค้นหาปฏิทิน
    def search_text(self, text):
        # แผนคือ สร้างปฏิทินขึ้นมาอีกอัน เป็นปฏิทินที่รวมเอาปฏิทินเคสจัดฟัน ปฏิทินเคสทั่วไป ปฏิทินเคสเลื่อน
        # รวมเข้ามาไว้อันเดียว โดยแปลงให้มี format ที่ถูกต้องคือ CNXXXXX คุณ XXXX XXX นัด XXXX
        # เพื่อให้ง่ายต่อการค้นหา ทำการค้นหาในปฏิทินรวม ออกมาแล้วให้อ่านโดยมี ข้อมูล คำค้นหา 'วันนัด', 'เวลานัด',
        # 'นัด', 'สถานะ', 'สร้างเมื่อ', 'อัพเดตเมื่อ', 'สร้างโดย', 'จัดการโดย'
        # self.search_cal(self, name_cal, text)
        pass

    # แจ้งตารางนัดหมายของวันที่ระบุ
    def event_in_day(self, date, *args):
        day_num = 1
        date_use = convert_time_thairead(convert_datestring(date))[:-6]
        head_of_all_cal = 'รายการนัดหมายของ วัน{}\n'.format(date_use)
        list_of_cal = []
        sep_between_event = "\n____________________________\n"
        for cal in args:
            name_cal = cal
            self.showDe = False
            cal_receive = self.get_limit(date, day_num, name_cal)
            object_read, new_list_of_event = read_dict_event(cal_receive, 'เวลานัด', 'นัด')
            if object_read:
                one_cal = ['ปฏิทิน: ' + new_list_of_event[0]['ปฏิทิน'], sep_between_event.join(object_read)]
                list_of_cal.append(sep_between_event.join(one_cal))
        sep_between_cal = "\n\n\n"
        return head_of_all_cal + sep_between_cal.join(list_of_cal)

    def event_create_in_day(self, date, *args):
        sep_between_event = "\n____________________________\n"
        all_last = []
        date_string = date
        for cal in args:
            name_cal = cal
            self.showDe = True
            cal_receive = self.get_last(0, name_cal)
            object_read, new_list_of_event = read_dict_event(cal_receive,
                                                             'อัพเดตเมื่อ',
                                                             'ปฏิทิน',
                                                             'วันนัด',
                                                             'เวลานัด',
                                                             'นัด',
                                                             'รายละเอียด',
                                                             'ลงสี',
                                                             'สถานะ',
                                                             'สร้างเมื่อ',
                                                             'อัพเดตเมื่อ')

            all_event_in_cal = sepread(object_read, new_list_of_event, date_string)
            if all_event_in_cal:
                all_last.append(sep_between_event.join(all_event_in_cal))
        last_out_put = '\n\n\n'.join(all_last)
        return last_out_put

    # ยังไม่เสร็จต้องเชื่อมกับฐานข้อมูล
    def show_noti(self, name_cal, syn):
        self.showDe = True
        cal_receive = self.get_onlymod(name_cal, syn)
        nextSync = cal_receive['nextSyncToken']
        object_read, new_list_of_event = read_dict_event(cal_receive, 'ปฏิทิน', 'วันนัด', 'เวลานัด', 'นัด',
                                                         'รายละเอียด', 'ลงสี', 'สถานะ', 'สร้าง', 'อัพเดต')
        date_string = datetime.datetime.now(timezone('Asia/Bangkok')).isoformat()[:10]
        all_event_in_cal = sepread(object_read, new_list_of_event, date_string)

    def push_noti(self, name_cal):
        self.showDe = True
        databa = WithDatabase(DATABASE_URL)
        syn = databa.get_last_token(name_cal)
        out_message = ''
        cal_receive = self.get_onlymod(name_cal, syn)
        if cal_receive:
            nextSync = cal_receive['nextSyncToken']
            date_string = datetime.datetime.now(timezone('Asia/Bangkok')).isoformat()[:10]
            databa.insert_token_new(date_string, name_cal, nextSync)
            object_read, new_list_of_event = read_dict_event(cal_receive, 'ปฏิทิน', 'วันนัด', 'เวลานัด', 'นัด',
                                                             'รายละเอียด', 'ลงสี', 'สถานะ', 'สร้าง', 'อัพเดต')
            all_event_in_cal = sepread(object_read, new_list_of_event, date_string)
            out_message = "\n".join(all_event_in_cal)
        return out_message