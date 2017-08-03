from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# parse json request
import simplejson
# generate and send captcha
from api.captcha import Captcha
from io import BytesIO
import base64
# send email
from django.core.mail import send_mail
# create user
from api.models import User
# password encrypt and decrypt
from Crypto.Hash import MD5
from Crypto.Cipher import AES


def get_captcha(request):
    f = BytesIO()
    img, code = Captcha.generate_captcha()
    img.save(f,'PNG')
    # 通过base64编码发送验证码图片
    return JsonResponse({
        'img': base64.b64encode(f.getvalue()).decode(),
        'captcha': str.lower(code)
    })

@csrf_exempt
def register(request):
    req = simplejson.load(request)
    email = req['email']
    password = req['password']
    nickname = req['nickname']
    users = User.objects.filter(email=email)
    user = User.objects.create_user(email=email, nickname=nickname, password=password)
    response = JsonResponse({ 'status': '1' })
    return response

@csrf_exempt
def captcha_email(request):
    '''获取请求中的email地址,发送邮件,返回状态码(0表示发送失败,1表示发送成功)和验证码答案'''
    req = simplejson.load(request)
    email = req['email']
    users = User.objects.filter(email=email)
    if len(users) != 0:
        response = JsonResponse({ 'status': '0'})
        return response
    else:
        captcha = ''.join(Captcha.string_captcha())
        msg = '您注册账户: [' + email + '] 的验证码是: ' + captcha
        mail_status = send_mail(
            r'[验证码]仨瓜俩枣小组的编程游戏',
            msg,
            'sagua_liazao@sohu.com',
            [email],
            fail_silently=False
            )
        response = JsonResponse({
            'status': '%s'%mail_status,
            'captcha': captcha
        })
        return response

def aes(request):
    # 生成秘钥的字符串,可以用验证码
    needed_string = 'abcdefg'
    key_md5 = MD5.new()
    key_md5.update(b'abcdefg')
    # 可以用于AES的key
    keyString = key_md5.hexdigest()
    print(keyString)
    ivString = keyString[2:18]
    print(ivString)
    # python需要使用'\0'来填充,否则加密得到的结果可能会butong
    # !shurufa huai le !
    PADDING = '\0'
    pad_it = lambda s: s + (16 - len(s) % 16) * PADDING
    data = '666666'

    # jiamiguocheng
    generator = AES.new(keyString, AES.MODE_CBC, ivString)
    crypt = generator.encrypt(pad_it(data))
    cryptedStr = base64.b64encode(crypt).decode()
    print(cryptedStr)

    # jiemiguocheng
    generator = AES.new(keyString, AES.MODE_CBC, ivString)
    # jiema dao bytes geshi
    recovery = generator.decrypt(crypt)
    # !!!zhe shi jie mi hui lai de zi fu chuan
    recovery_string = recovery.decode().rstrip(PADDING)
    # recovery = recovery.rstrip(PADDING)
    print(recovery_string)
    # print(recovery.rstrip(PADDING)
    return HttpResponse('hello')