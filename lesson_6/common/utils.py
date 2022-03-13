from socket import *
from .variables import *
import time
import json
from common.decorators import log

@log
def get_message(socket):
    msg = socket.recv(MSG_LENGTH)
    # print('msg_rec', msg)
    if isinstance(msg, bytes):
        msg_decode = msg.decode(ENCODING)
        msg_json = json.loads(msg_decode)
        type(msg_json)
        if isinstance(msg_json, dict):
            return msg_json
        raise ValueError
    raise ValueError

@log
def send_message(socket, msg):
    msg_json = json.dumps(msg)
    # print(msg_json)
    msg_encode = msg_json.encode(ENCODING)
    socket.send(msg_encode)
    print('Сообщение отправлено')