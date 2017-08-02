from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson
from api.captcha import Captcha
from io import BytesIO
import base64
from django.core.mail import send_mail
from api.models import User

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
    users = User.objects.filter(email=email)
    user = User.objects.create_user(email=email, nickname='', password=password)
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