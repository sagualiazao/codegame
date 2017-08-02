from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson
from api.captcha import Captcha
from io import BytesIO
import base64
from django.core.mail import send_mail

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
    response = JsonResponse({
        'msg': email + ' ' + password
    })
    return response

def captcha_email(request):
    captcha = ''.join(Captcha.string_captcha())
    msg = '您注册账户:' + '的验证码是:' + captcha
    response = send_mail(
        r'[验证码]仨瓜俩枣小组的编程游戏',
        msg,
        'sagua_liazao@sohu.com',
        ['834946220@qq.com'],
        fail_silently=False
        )
    return HttpResponse('%s'%response)