from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FileMessage
)

from wit import Wit
from collections import namedtuple
import deepcut
import os
import psycopg2
import random


# Wit.ai parameters
sen = os.environ.get('SEN')
cm = os.environ.get('CM')
cg = os.environ.get('CG')
mc = os.environ.get('MC')
hs = os.environ.get('HS')
sf = os.environ.get('SELF')

DATABASE_URL = os.getenv('DATABASE_URL')
AccessToken = os.getenv('AccessToken')
ChannelSecret = os.getenv('ChannelSecret')

app = Flask(__name__)

line_bot_api = LineBotApi(AccessToken)
handler = WebhookHandler(ChannelSecret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
        print(body)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    def extract_value(inp_text, wit_token):
        understanding = Wit(wit_token)
        token_input_text = deepcut.tokenize(inp_text)
        deep = understanding.message(" ".join(token_input_text))

        try:
            intent_value = deep['data'][0]['__wit__legacy_response']['entities']['intent'][0]['value']
            intent_confident = deep['data'][0]['__wit__legacy_response']['entities']['intent'][0]['confidence']
        except KeyError:
            try:
                intent_value = deep['entities']['intent'][0]['value']
                intent_confident = deep['entities']['intent'][0]['confidence']
            except KeyError:
                intent_value = deep['entities']
                intent_confident = deep['entities']
        return intent_value, intent_confident

    def message(mes):
        return mes.split(', ')

    def message_with_con(a, con):
        if con > 0.8:
            s = ['แน่นอนว่า', 'ฉันมั่นใจว่า', 'ไม่ต้องสงสัยเลย']
            n = [', ', ', ', '']
            mes = random.choice(s) + random.choice(n) + a
            b = mes.split(', ')
        elif 0.6 < con <= 0.8:
            s = ['คิดว่า', 'ฉันว่า', 'ฉันรู้ว่า']
            n = [', ', ', ', '']
            mes = random.choice(s) + random.choice(n) + a
            b = mes.split(', ')
        elif 0.4 < con <= 0.6:
            s = ['ไม่ค่อยมั่นใจว่า', 'ไม่ค่อยมั่นใจนะว่า', 'ฉันไม่แน่ใจนะว่า']
            n = [', ', ', ', '']
            mes = random.choice(s) + random.choice(n) + a
            b = mes.split(', ')
        else:
            s = ['ฉันไม่แน่ใจว่า', 'ไม่ค่อยมั่นใจเลยว่า', 'ฉันไม่แน่ใจ แต่ก็คิดว่า']
            n = n = [', ', ', ', '']
            mes = random.choice(s) + random.choice(n) + a
            b = mes.split(', ')
        return b

    def choose_mode(inp_text, wit_token):
        value, confident = extract_value(inp_text, wit_token)
        chm = namedtuple('out', 'text pur')
        if value == 'อยากเล่นเกม':
            output = message("อยากเล่นเกมอะไรนะ")
            choose = 1
        elif value == 'ทักทาย':
            output = message("สวัสดี ฉันชื่อบริน, ฉันชอบเล่นเกม, วันนี้คุณอยากเล่นเกมไหม")
            choose = 0
        elif value == 'สนทนาทั่วไป':
            output = message("ฉันเดาว่าคุณแค่อยากคุยกับฉันเฉย ๆ ใช่ไหม")
            choose = 4
        elif value == 'มีคำแนะนำ':
            output = message('คุณว่าฉันทำไม, คุณมีอะไรแนะนำฉันอีกไหม')
            choose = 4
        else:
            output = message("คุณอยากจะทำอะไร, จะเล่นเกมไหม, หรือจะคุยเล่น ๆ, หรือจะแนะนำอะไรให้ฉันไหม")
            choose = 4
        return chm(text=output, pur=choose)

    def choose_game(inp_text, wit_token):
        value, confident = extract_value(inp_text, wit_token)
        sen_type, confident1 = extract_value(inp_text, sen)
        chm = namedtuple('out', 'text pur')
        if sen_type == 'ถาม':
            output = message("ฉันถามคุณก่อนนะ, ถ้าไม่อยากเล่นก็ไม่เป็นไร, ฉันไม่บังคับ")
            choose = 1
        elif value == 'เล่นทายใจ':
            output = message('โอเค, งั้นเล่นทายใจ, ถ้าอยากเลิกเล่นตอนไหนให้พิมพ์ว่า เลิกเล่น นะ')
            choose = 2
        elif value == 'เล่นจับโกหก':
            output = message('เล่นจับโกหกเหรอ, ว่ามาเลย, ถ้าอยากเลิกเล่นตอนไหนให้พิมพ์ว่า เลิกเล่น นะ')
            choose = 3
        elif value == 'เล่นโต้เถียง':
            output = message(
                'ขออภัย ฉันยังเล่นโต้เถียงไม่ได้, กรุณาเลือกเกมใหม่')
            choose = 1
        elif value == 'ไม่เล่น':
            output = message('ก็ได้, ละอยากทำอะไร')
            choose = 0
        else:
            output = message('บอกฉันที คุณอยากเล่นอะไร, มีเกมทายใจ และเกมจับโกหกให้เลือกนะ')
            choose = 1
        return chm(text=output, pur=choose)

    def happy_sad(inp_text, wit_token):
        value, confident = extract_value(inp_text, wit_token)

        value1, confident1 = extract_value(inp_text, sf)
        value2, confident2 = extract_value(inp_text, sen)
        chm = namedtuple('out', 'text pur')
        if inp_text == 'เลิกเล่น':
            output = message("ไม่เล่นทายใจแล้วหรือ, ถ้างั้นเล่นอะไรดีล่ะ")
            choose = 1
        elif value1 == 'Me' and value2 == 'ชม':
            output = message("ขอบคุณที่ชม, พิมพ์ต่อเลยนะ")
            choose = 2
        elif value1 == 'Me' and value2 == 'ว่า':
            output = message("คุณว่าฉันทำไม, คุณจะเลิกเล่นก็ได้, พิมพ์ว่าเลิกเล่นสิ")
            choose = 2
        elif value1 == 'Me' and value2 == 'ถาม':
            output = message("คุณถามฉันเหรอ, ฉันก็ไม่รู้จะถามใครต่อดี")
            choose = 2
        elif value1 == 'Me':
            output = message("พิมพ์เรื่องของคุณดีกว่า, เรากำลังเล่นเกมอยู่นะ")
            choose = 2
        elif value1 == 'Other':
            output = message("เกมนี้ฉันทายว่าคุณความสุขไหม, คุณก็ต้องพิมพ์เรื่องของตัวเองสิ, "
                             "พิมพ์ประโยคต่อไปเลยฉันจะทาย")
            choose = 2
        elif value == 'สุข':
            output = message_with_con('นั่นทำให้คุณมีความสุข', confident)
            choose = 2
        elif value == 'ทุกข์':
            output = message_with_con('นั่นทำให้คุณเป็นทุกข์', confident)
            choose = 2
        elif value == 'เฉยๆ':
            output = message_with_con('นั่นทำให้คุณเฉยๆ', confident)
            choose = 2
        else:
            output = message('ไม่รู้เหมือนกัน อ่ะเล่นต่อ')
            choose = 2
        return chm(text=output, pur=choose)

    def true_false(inp_text, wit_token):
        value, confident = extract_value(inp_text, wit_token)
        value1, confident1 = extract_value(inp_text, sen)

        chm = namedtuple('out', 'text pur')
        if inp_text == 'เลิกเล่น':
            output = message('เบื่อแล้วเหรอ งั้นเล่นอะไรต่อดี')
            choose = 1
        elif value == 'มุสา':
            output = message_with_con('คุณโกหก', confident)
            choose = 3
        elif value == 'อาจจริง':
            output = message_with_con('เรื่องนี้เป็นไปได้', confident)
            choose = 3
        else:
            output = message('ไม่รู้เลยว่าโกหกหรือจริง แปลกมาก')
            choose = 3
        return chm(text=output, pur=choose)

    def simple_con(inp_text, wit_token):
        value, confident = extract_value(inp_text, wit_token)
        s = ['ว่า', 'บอกเล่า', 'ตอบ', 'แสดงความต้องการ', 'คำสั่ง', 'ทักทาย', 'ชม', 'ถาม']
        chm = namedtuple('out', 'text pur')
        if 'อยาก' in inp_text:
            output = message('ต้องการทำอะไรนะ')
            choose = 0
        elif value in s:
            output = message("ข้อความที่ส่งมาคือการ " + value + ", ถ้าคุณต้องการให้ฉันเลิกวิเคราะห์ประโยคของคุณ "
                                                                "โปรดพิมพ์คำไหนก็ได้ที่มีคำว่าอยาก")
            choose = 4
        else:
            output = message('ไม่รู้ว่าข้อความนี้เป็นข้อความประเภทไหน, ถ้าคุณต้องการให้ฉันเลิกวิเคราะห์ประโยคของคุณ '
                             'โปรดพิมพ์คำไหนก็ได้ที่มีคำว่าอยาก')
            choose = 4
        return chm(text=output, pur=choose)

    def test(b, fb_id):
        extract_value(b, sen)
        global conn
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS fores (who text, send text, receiver text, mode integer, time TIMESTAMP "
            "NOT NULL);")
        conn.commit()

        # ตรวจสอบข้อความที่ถูกส่งมาว่า เป็นข้อความเดียวกันหรือไม่
        cur.execute("SELECT send FROM fores WHERE who = %(str)s ORDER BY time DESC LIMIT 1;", {'str': fb_id})
        text_from_user1 = cur.fetchall()
        conn.commit()

        cur.execute("INSERT INTO fores (who, send, receiver, mode, time) VALUES (%(person1)s, %(wd)s, %(person2)s, "
                    "%(int)s, NOW());", {'person1': fb_id, 'wd': b, 'person2': "me", 'int': 9})
        conn.commit()

        cur.execute("SELECT send FROM fores WHERE who = %(str)s ORDER BY time DESC LIMIT 1;", {'str': fb_id})
        text_from_user2 = cur.fetchall()
        conn.commit()

        # ถ้าไม่ใช่ข้อความเดียวกับที่เคยส่งแล้ว ระบบจะนำไปประมวลผลเพื่อตอบ
        if text_from_user1 != text_from_user2:
            print("system will response because it not the same message")
            # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
            cur.execute("SELECT mode FROM fores WHERE receiver = %(str)s ORDER BY time DESC LIMIT 1;", {'str': fb_id})
            m = cur.fetchall()
            conn.commit()

            try:
                n = int(str(m)[2])
            except IndexError:
                n = 0
            mode_app = n
            if mode_app == 0:
                alpha = choose_mode(b, cm)
                resp_word = alpha.text
                purpose = alpha.pur
            elif mode_app == 1:
                alpha = choose_game(b, cg)
                resp_word = alpha.text
                purpose = alpha.pur
            elif mode_app == 2:
                alpha = happy_sad(b, hs)
                resp_word = alpha.text
                purpose = alpha.pur
            elif mode_app == 3:
                alpha = true_false(b, mc)
                resp_word = alpha.text
                purpose = alpha.pur
            else:
                alpha = simple_con(b, sen)
                resp_word = alpha.text
                purpose = alpha.pur
            a = []
            for word in resp_word:
                # หยิบสิ่ง me ส่งล่าสุดมาใส่ในตัวแปร last_word แล้วเทียบกับสิ่งที่จะส่งอีกครั้งว่าซ้ำกันหรือไม่
                # ป้องกันการส่งข้อความซ้ำ
                cur.execute("SELECT send FROM fores WHERE who = %(str)s ORDER BY time DESC LIMIT 1;", {'str': "me"})
                m = cur.fetchall()
                conn.commit()

                last_word = str(m)[3:-4]
                if word != last_word:
                    a.append(TextSendMessage(text=word))

                    # หลังจากส่งข้อความไปแล้ว นำข้อความที่ส่งใส่เข้าไปใน fores
                    cur.execute("INSERT INTO fores (who, send, receiver, mode, time) VALUES (%(person1)s, %(wd)s, "
                                "%(person2)s, %(int)s, NOW());",
                                {'person1': "me", 'wd': word, 'person2': fb_id, 'int': purpose})
                    conn.commit()
                else:
                    pass
            line_bot_api.reply_message(
                event.reply_token, a)
            cur.close()
            conn.close()
        else:
            print("system will not response because it is the same message")

    who = event.source.user_id
    user_word = event.message.text
    test(user_word, who)


if __name__ == "__main__":
    app.run()
