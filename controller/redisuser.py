import json
import re

from flask import Blueprint, request, session
from model.user import User
from common.redisdb import redis_connect
user = Blueprint('user', __name__)

redis_client = redis_connect()
def gen_emial_code():
    return ''

@user.route('/redis/ecode', methods=['post'])
def get_one():
    email = json.loads(request.data('email'))
    if not re.match(".+@.+\..+", email):
        return '邮箱无效'
    code = gen_emial_code()

    try:
        # send_emial(emial, code)
        # session['ecode'] = code.lower()
        email_vcode = 'email' + code.lower()
        redis_client.set('email', code.lower())
        # 单独设置过期时间
        redis_client.expire(email_vcode, 60)

        # 存在redis
        return '邮件发送成功'
    except Exception as e:
        print(e)
        return '邮件发送失败'
    return '验证码'