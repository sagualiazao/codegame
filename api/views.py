from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import simplejson
from api.utils import *
from django.core.mail import send_mail
from api.models import User, DesignedMaps, GameLevels


def get_captcha(request):
    """
    向web前端发送图片验证码

    Parameters:
        :request: 指向'/api/captcha'的GET请求\n

    Returns:
        JsonResponse:\n
        :'img': 图片验证码的base64编码\n
        :'capthca': 验证码的小写字符串\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    if request.method == 'GET':
        img, code = Captcha.base64_captcha()
        return JsonResponse({
            'img': img,
            'captcha': code,
        })
    else:
        return HttpResponseNotFound()


@csrf_exempt
def register(request):
    """
    执行注册用户操作

    Parameters:
        :request: 指向'/api/register'的POST请求\n

    Returns:
        JsonResponse:\n
        :'status': 注册失败'0', 注册成功'1'\n
        :'capthca': 验证码的小写字符串\n

        HttpResponseNotFound(): 如果request不是一个POST请求\n
    """
    if request.method == 'POST':
        try:
            req = simplejson.load(request)
            email = req['email']
            if check_email_format(email) == False:
                return SimpleResponse.failure_json_response
            if len(User.objects.filter(email=email)) > 0:
                return SimpleResponse.failure_json_response
            password_ace = req['password']
            nickname = req['nickname']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            User.objects.create_user(email=email, nickname=nickname, password=password)
        except BaseException:
            return SimpleResponse.failure_json_response
        else:
            return SimpleResponse.success_json_response
    else:
        return HttpResponseNotFound()


@csrf_exempt
def reset_password_email(request):
    """
    发送重置密码的邮件验证码

    Parameters:
        :request: 指向'/api/reset-password-email'的POST请求\n

    Returns:
        JsonResponse:\n
        :'status': 发送失败'0', 发送成功'1'\n
        :'capthca': 验证码的小写字符串\n

        HttpResponseNotFound(): 如果request不是一个POST请求\n
    """
    if request.method == 'POST':
        try:
            req = simplejson.load(request)
            email = req['email']
            users = User.objects.filter(email=email)
            if len(users) == 0:
                return SimpleResponse.failure_json_response
            captcha = Captcha.string_captcha()
            msg = '您重置账户: [' + email + '] 密码的验证码是: ' + captcha
            mail_status = send_mail(
                r'[验证码]仨瓜俩枣小组的编程游戏-密码重置',
                msg,
                'sagualiazao@aliyun.com',
                [email],
                fail_silently=False
            )
            request.session['captcha'] = captcha
        except BaseException:
            return SimpleResponse.failure_json_response
        return SimpleResponse.success_json_response
    else:
        return HttpResponseNotFound()


def check_email_captcha(request):
    """
    建议输入的邮件验证码是否正确

    Parameters:
        :request: 指向'/api/check-email'的GET请求\n

    Returns:
        JsonResponse:\n
        :'status': 未被注册'0', 已被注册'1'\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    if request.method == 'GET':
        try:
            captcha = request.GET['captcha']
            if captcha != request.session['captcha']:
                return SimpleResponse.failure_json_response
            else:
                return SimpleResponse.success_json_response
        except BaseException:
            return SimpleResponse.failure_json_response
    else:
        return HttpResponseNotFound()


@csrf_exempt
def reset_password(request):
    """
    重置密码

    Parameters:
        :request: 指向'/api/reset-password'的POST请求\n

    Returns:
        JsonResponse:\n
        :'status': 修改失败'0', 修改成功'1'\n

        HttpResponseNotFound(): 如果request不是一个POST请求\n
    """
    if request.method == 'POST':
        try:
            # 捕获json为空错误
            req = simplejson.load(request)
            email = req['email']
            users = User.objects.filter(email=email)
            # 如果该用户不存在,不需要检查邮箱格式
            if len(users) == 0:
                return SimpleResponse.failure_json_response
            # 捕获值缺少或错误
            password_ace = req['password']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            user = users[0]
            user.set_password(password)
            user.save()
        except BaseException:
            return SimpleResponse.failure_json_response
        return SimpleResponse.success_json_response
    else:
        return HttpResponseNotFound()


@csrf_exempt
def login(request):
    """
    登录

    Parameters:
        :request: 指向'/api/login'的POST请求或GET请求\n
    Returns:
        JsonResponse:\n
        :'status': 登录失败'0', 登录成功'1'\n
        :'email': 用户的电子邮件\n
        :'nickname': 用户的昵称\n
        :'id': - 用户的id\n
        :'gameProgress': 用户的游戏进度\n
        :'hasPaied': 用户是否已经付费\n

        HttpResponseNotFound(): 如果request不是一个POST\GET请求\n
    """
    # POST请求来自主动登录
    if request.method == 'POST':
        try:
            req = simplejson.load(request)
            email = req['email']
            users = User.objects.filter(email=email)
            if len(users) == 0:
                return SimpleResponse.failure_json_response
            password_ace = req['password']
            captcha = req['captcha']
            password = CBC.decrypt(captcha, password_ace)
            user = users[0]
            login_status = user.check_password(password)
        except BaseException:
            return SimpleResponse.failure_json_response
        else:
            if login_status:
                request.session['email'] = email
                return SimpleResponse.user_json_response(user)
            else:
                return SimpleResponse.failure_json_response
    # GET请求来自登录状态检测
    elif request.method == 'GET':
        email = request.session.get('email', False)
        if email == False:
            return SimpleResponse.failure_json_response
        else:
            users = User.objects.filter(email=email)
            user = users[0]
            return SimpleResponse.user_json_response(user)
    else:
        return HttpResponseNotFound()


def check_email(request):
    """
    检验邮箱是否已被注册

    Parameters:
        :request: 指向'/api/check-email'的POST请求或GET请求\n

    Returns:
        JsonResponse:\n
        :'status': - 未被注册'0', 已被注册'1'\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    if request.method == 'GET':
        try:
            email = request.GET['email']
            users = User.objects.filter(email=email)
        except BaseException:
            return SimpleResponse.failure_json_response
        else:
            if len(users) == 0:
                return SimpleResponse.failure_json_response
            else:
                return SimpleResponse.success_json_response
    else:
        return HttpResponseNotFound()

def logout(request):
    """
    注销

    Parameters:
        :request: 指向'/api/logout'的GET请求\n

    Returns:
        JsonResponse:\n
        :'status': 注销失败'0', 注销成功'1'\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    if request.method == 'GET':
        email = request.session.get('email', False)
        if email == False:
            return SimpleResponse.failure_json_response
        else:
            del request.session['email']
            return SimpleResponse.success_json_response
    else:
        return HttpResponseNotFound()

@csrf_exempt
def save_map(request):
    """
    保存用户编辑的地图

    Parameters:
        :request: 指向'/api/save-map'的POST请求\n
        :mapString: 要存储的地图信息\n
        :name: 地图的名称\n
        :remarks: 地图的说明\n

    Returns:
        JsonResponse:\n
        :'status': 保存失败'0', 保存成功'1'\n

        HttpResponseNotFound(): 如果request不是一个POST请求\n
    """
    if request.method == 'POST':
        try:
            req = simplejson.load(request)
            email = request.session['email']
            author = User.objects.get(email=email)
            map_str = req['mapString']
            name = req['name']
            remarks = req['remarks']
            newMap = DesignedMaps(
                map=map_str,
                name=name,
                remarks=remarks,
                author=author,
                is_published=False
            )
            newMap.save()
            status = MapImage.generate_map_image(newMap.map_id, map_str)
        except BaseException:
            return SimpleResponse.failure_json_response
        else:
            return SimpleResponse.success_json_response
    else:
        return HttpResponseNotFound()


@csrf_exempt
def read_map(request):
    """
    读取用户编辑的地图

    Parameters:
        :request: 指向'/api/read-map'的GET请求\n
        :mapid: 要读取的map的id\n

    Returns:
        JsonResponse:\n
        :'status': 读取失败'0', 读取成功'1'\n
        :'map': 地图字符串\n
        :'name': 地图名\n
        :'remarks': 地图说明\n
        :'author': 地图作者\n
        :'is_published': 地图发布状态\n

        HttpResponseNotFound(): 如果request不是一个GET请求\n
    """
    if request.method == 'GET':
        try:
            map_id = int(request.GET['mapid'])
            selected_map = DesignedMaps.objects.filter(map_id=map_id)
            if len(selected_map) == 0:
                return SimpleResponse.failure_json_response
            else:
                selected_map = selected_map[0]
                return SimpleResponse.designed_map_json_response(selected_map)
        except BaseException as e:
            return SimpleResponse.failure_json_response
    else:
        return HttpResponseNotFound()

@csrf_exempt
def pay(request):
    """
    发送支付请求

    Parameters:
        :request: 指向'/api/pay'的GET请求,需要服务器保存session信息(已登录)才能访问\n

    Returns:
        JsonResponse:\n
        :'status': 发送支付请求失败'0',发送成功'1'\n
        :'url': 成功发送支付请求打开的页面\n
    """
    if request.method == 'GET':
        email = request.session.get('email', False)
        if email == False:
            return HttpResponseNotFound()
        else:
            try:
                users = User.objects.filter(email=email)
                user = users[0]
                alipay_pr = Pingpp.pay()
                return JsonResponse({
                    'status': '1',
                    'url': alipay_pr
                })
            except BaseException:
                return SimpleResponse.failure_json_response
    else:
        return SimpleResponse.failure_json_response
