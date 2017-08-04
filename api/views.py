from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson
from api.captcha import Captcha
from io import BytesIO
import base64
from django.core.mail import send_mail
from api.models import User
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import api.cbc as CBC


def get_captcha(request):
    '''
        接受指向'/api/captcha'的GET请求,返回验证码图片的base64编码'img'和对应字符串'captcha'
    '''
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
    '''
        接受指向'/api/register'的POST请求,在数据库中注册用户,成功的话返回'status'状态码'1'
    '''
    req = simplejson.load(request)
    email = req['email']
    # 接受到的password是经过前端CBC加密后的字符串
    password_ace = req['password']
    nickname = req['nickname']
    captcha = req['captcha']
    password = CBC.decrypt(captcha, password_ace)
    user = User.objects.create_user(email=email, nickname=nickname, password=password)
    response = JsonResponse({ 'status': '1' })
    return response

def send_email(request, title, msg):
    '''
        获取请求中的'email'地址,发送邮件,标题为'title',消息内容为'msg'\n
        返回状态码'status'('0'表示当前邮箱尚未注册,'1'表示发送成功)和验证码答案'captcha'
    '''
    req = simplejson.load(request)
    email = req['email']
    users = User.objects.filter(email=email)
    if len(users) != 0:
        response = JsonResponse({ 'status': '0'})
        return response
    else:
        captcha = ''.join(Captcha.string_captcha())
        msg = '您好,[' + email + ']!\n' + msg + captcha
        mail_status = send_mail(
            title,
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


@csrf_exempt
def captcha_email(request):
    '''
        获取请求中的email地址,发送邮件,返回'status'状态码('0'表示发送失败/邮箱已被注册,'1'表示发送成功)和验证码答案'captcha'
    '''
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
            r'[验证码]仨瓜俩枣小组的编程游戏-新用户注册',
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

@csrf_exempt
def reset_password_email(request):
    '''
        获取请求中的email地址,发送邮件,返回'status'状态码('0'表示邮箱未被注册,'1'表示发送成功)和验证码答案'captcha'
    '''
    req = simplejson.load(request)
    email = req['email']
    users = User.objects.filter(email=email)
    if len(users) == 0:
        response = JsonResponse({ 'status': '0'})
        return response
    else:
        captcha = ''.join(Captcha.string_captcha())
        msg = '您重置账户: [' + email + '] 密码的验证码是: ' + captcha
        mail_status = send_mail(
            r'[验证码]仨瓜俩枣小组的编程游戏-密码重置',
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

@csrf_exempt
def reset_password(request):
    '''
        接收一个POST请求: request\n
        包含'email','captcha',加密后的'password'
        接受请求中的'email'地址和'captcha',将对应账户的密码设为'password'\n
        修改成功,返回status='1',否则返回'status'='0'
    '''
    if request.method == 'GET':
        return HttpResponse(
            'This request is designed to reset your password, but you should send a POST request!'
            )
    elif request.method == 'POST':
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            response = JsonResponse({ 'status': '0'})
            return response
        else:
            password_ace = req['password']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            user = users[0]
            user.set_password(password)
            user.save()
            response = JsonResponse({ 'status': '1'})
            return response

@csrf_exempt
def login(request):
    '''
        接受一个POST请求:request\n
        包含'email', 'captcha'和加密后的'password'\n
        接受请求中的email和password,检验是否匹配\n
        如果匹配(登录成功),返回status='1',否则返回'0'
    '''
    if request.method == 'GET':
        return HttpResponse(
            'This request is designed to login your account, but you should send a POST request!'
            )
    elif request.method == 'POST':
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            response = JsonResponse({ 'status': '0'})
            return response
        else:
            password_ace = req['password']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            user = users[0]
            login_status = user.check_password(password)
            if login_status:
                
                return JsonResponse({
                    'status': '1',
                    'email': user.email,
                    'nickname': user.nickname,
                    'id': user.id,
                    'gameProgress': user.game_progress,
                    'hasPaied': user.has_paied
                    })
            else:
                return JsonResponse({ 'status': '0'})


@csrf_exempt
def test(request):
    # 用于测试新的api
    return HttpResponse('hello')

