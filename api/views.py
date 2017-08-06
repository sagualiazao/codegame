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
        @param :request:指向'/api/captcha'的GET请求\n
        @return :JsonResponse:\n
        :img:验证码图片的base64编码\n
        :captcha:验证码对应字符串
    '''
    if request.method == 'GET':
        f = BytesIO()
        img, code = Captcha.generate_captcha()
        img.save(f,'PNG')
        # 通过base64编码发送验证码图片
        return JsonResponse({
            'img': base64.b64encode(f.getvalue()).decode(),
            'captcha': str.lower(code)
        })
    else:
        return HttpResponse('GET please!')

@csrf_exempt
def register(request):
    '''
        @param :request:指向'/api/register'的POST请求\n
        在数据库中注册用户\n
        @return :JsonResponse:\n
        :status: 注册成功'1',注册失败'0'
    '''
    if request.method == 'POST':
        try:
            req = simplejson.load(request)
            email = req['email']
            # 接受到的password是经过前端CBC加密后的字符串
            password_ace = req['password']
            nickname = req['nickname']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            user = User.objects.create_user(email=email, nickname=nickname, password=password)
        except BaseException:
            return JsonResponse({ 'status': '0' })
        else:
            return JsonResponse({ 'status': '1' })
    else:
        return HttpResponse('POST please!')

@csrf_exempt
def captcha_email(request):
    '''
        @param :request:指向'/api/captcha-email'的POST请求\n
        获取请求中的email地址,发送邮件
        @return :JsonResponse:\n
        :status: 表示邮箱已被注册'0',发送成功'1',发送失败'2'\n
        :captcha:验证码答案
    '''
    if request.method == 'POST':
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) != 0:
            return JsonResponse({ 'status': '0' })
        else:
            captcha = ''.join(Captcha.string_captcha())
            msg = '您注册账户: [' + email + '] 的验证码是: ' + captcha
            try:
                mail_status = send_mail(
                    r'[验证码]仨瓜俩枣小组的编程游戏-新用户注册',
                    msg,
                    'sagualiazao@aliyun.com',
                    [email],
                    fail_silently=False
                    )
            except BaseException:
                return JsonResponse({ 'status': '2' })
            else:
                return JsonResponse({
                    'status': '%s'%mail_status,
                    'captcha': captcha
                })
    else:
        return HttpResponse('POST please!')

@csrf_exempt
def reset_password_email(request):
    '''
       @param :request:指向'/api/reset-password-email'的POST请求\n
       获取请求中的email地址,发送邮件\n
       @return JsonResponse\n
       :status: '0'表示邮箱未被注册,'1'表示发送成功,发送失败'2'\n
       :captcha: 验证码答案
    '''
    if request.method == 'POST':
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            response = JsonResponse({ 'status': '0' })
            return response
        else:
            captcha = ''.join(Captcha.string_captcha())
            msg = '您重置账户: [' + email + '] 密码的验证码是: ' + captcha
            try:
                mail_status = send_mail(
                    r'[验证码]仨瓜俩枣小组的编程游戏-密码重置',
                    msg,
                    'sagualiazao@aliyun.com',
                    [email],
                    fail_silently=False
                    )
            except BaseException:
                return JsonResponse({ 'status': '2' })
            else:
                response = JsonResponse({
                    'status': '%s'%mail_status,
                    'captcha': captcha
                })
                return response
    else:
        return HttpResponse('POST please!')

@csrf_exempt
def reset_password(request):
    '''
        @param :request:接收一个指向'/api/reset-password'的POST请求\n
        包含'email','captcha',加密后的'password'\n
        接受请求中的'email'地址和'captcha',将对应账户的密码设为'password'\n
        @return :Jsonresponse:\n
        :status: 修改成功返回'1',否则返回'0'
    '''
    if request.method == 'POST':
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            response = JsonResponse({ 'status': '0' })
            return response
        else:
            try:
                password_ace = req['password']
                captcha = req['captcha']
                password = CBC.decrypt(captcha, password_ace)
                user = users[0]
                user.set_password(password)
                user.save()
            except BaseException:
                return JsonResponse({ 'status': '0' })
            else:
                return JsonResponse({ 'status': '1' })
    else:
        return HttpResponse('POST please!')

@csrf_exempt
def login(request):
    '''
        @param :request:接受一个指向'/api/login'的POST请求\n
        包含'email', 'captcha'和加密后的'password'\n
        接受请求中的email和password,检验是否匹配\n
        @return :JsonResponse:
        :status:如果匹配(登录成功)返回'1',否则返回'0'
    '''
    if request.method == 'POST':
        print(request.session.get('email', False))
        req = simplejson.load(request)
        email = req['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            response = JsonResponse({ 'status': '0'})
            return response
        else:
            try:
                password_ace = req['password']
                captcha = req['captcha']
                password = CBC.decrypt(captcha, password_ace)
                user = users[0]
                login_status = user.check_password(password)
            except BaseException:
                return JsonResponse({ 'status': '0' })
            else:
                if login_status:
                    request.session['email'] = email
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
    else:
        return HttpResponse('POST please!')

@csrf_exempt
def test(request):
    '''
        用于测试新的api(GET)
    '''
    # 用于测试新的api
    return HttpResponse('hello')

